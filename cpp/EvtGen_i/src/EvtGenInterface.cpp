//
// Copyright (C) 2018-2020 BINP for the benefit of the SCTau collaboration
//
#include "EvtGen_i/EvtGenInterface.h"

// EvtGen
#define EVTGEN_CPP11
#include "EvtGen/EvtGen.hh"
#include "EvtGenBase/EvtRandom.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtHepMCEvent.hh"
#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtParticleFactory.hh"
#include "EvtGenBase/EvtMTRandomEngine.hh"
#include "EvtGenExternal/EvtExternalGenList.hh"
#include "EvtGenExternal/EvtPHOTOS.hh"

#include "PathResolver/PathResolver.h"

// HepMC
#include "HepMC/GenEvent.h"

#include <iostream>
#include <cmath>

DECLARE_COMPONENT(EvtGenInterface)

EvtGenInterface::EvtGenInterface(const std::string& type,
                                 const std::string& name,
                                 const IInterface* parent) :
    AuroraTool(type, name, parent) {}

StatusCode EvtGenInterface::initKinematics() {
    m_energy = m_ecms.value() < 0.01 ?
               EvtPDL::getMass(m_rootParticle) :
               m_ecms.value();
    if (m_energy < 0.01) {
        error() << "EvtGen: zero CMS energy" << endmsg;
        return StatusCode::FAILURE;
    }

    const double mElec = EvtPDL::getMass(EvtId(11, 11)) * 0.001;
    info() << "Electron mass: " << mElec << endmsg;
    const double mElecSq = mElec*mElec;

    c_ideal_electron_momentum = EvtVector3R{
        0.25*m_angle*1.e-3*m_energy, 0, sqrt(0.25*m_energy*m_energy - mElecSq)};
    c_ideal_positron_momentum = c_ideal_electron_momentum;
    c_ideal_positron_momentum.set(2, -c_ideal_electron_momentum.get(2));

    info() << "Beams initialized for sqrt(s) = " << m_energy << ":\n"
           << "    X angle: " << m_angle << " mrad\n"
           << "  Electrons: ("
           << c_ideal_electron_momentum.get(0) << ", "
           << c_ideal_electron_momentum.get(1) << ", "
           << c_ideal_electron_momentum.get(2) << ")\n"
           << "  Positrons: ("
           << c_ideal_positron_momentum.get(0) << ", "
           << c_ideal_positron_momentum.get(1) << ", "
           << c_ideal_positron_momentum.get(2) << ")" << endmsg;
    return StatusCode::SUCCESS;
}

StatusCode EvtGenInterface::initialize() {
    auto sc = AuroraTool::initialize();
    if (!sc.isSuccess()) return sc;

    m_rndm = std::make_unique<EvtMTRandomEngine>(m_rndm_seed);
    m_genList = std::make_unique<EvtExternalGenList>();
    m_exmodels = m_genList->getListOfModels();

    rd = std::make_unique<std::random_device>();

    info() << "Builtin external models" << endmsg;

    for (auto& toolname : m_modelToolNames) {
        info() << "Retrieving external model " << toolname << endmsg;
        ToolHandle<IEvtGenModel> _tool(toolname);
        StatusCode sc = _tool.retrieve();
        if (sc.isSuccess()) {
            m_addon_models.push_back(_tool.get());
        } else {
            error() << "Unable to retrieve the model '" << toolname << "'." << endmsg;
            return StatusCode::FAILURE;
        }
    }

    info() << "Custom external models" << endmsg;

    for (auto& amodel: m_addon_models) {
        m_exmodels.push_back(amodel->getModel());
    }

    info() << "List of external models: " << endmsg;
    for (const auto& model : m_exmodels)
        info() << model->getName() << endmsg;

    m_evtgen = std::make_unique<EvtGen>(
        PathResolverFindDataFile(m_decdec).c_str(),
        PathResolverFindDataFile(m_evtpdl).c_str(),
        m_rndm.get(),
        m_genList->getPhotosModel(),
        &m_exmodels
    );

    EvtRandom::setRandomEngine(m_rndm.get());
    if (!m_usrdec.empty())
        m_evtgen->readUDecay(PathResolverFindDataFile(m_usrdec).c_str());

    m_rootParticle = EvtPDL::getId(m_rootpcl.value());
    return initKinematics();
}

StatusCode EvtGenInterface::finalize() {
    return AuroraTool::finalize();
}

EvtVector3R EvtGenInterface::random_unit_vector3d() const {
    static std::mt19937 gen{(*rd)()};
    static std::uniform_real_distribution<double> uni(0.0, 1.0);

    double phi = uni(gen) * M_PI * 2.;
    double sinphi = std::sin(phi);
    double cosphi = std::cos(phi);
    double costh = uni(gen);
    double sinth = std::sqrt(1. - costh*costh);

    return {sinth*cosphi, sinth*sinphi, sinth};
}

double energy(double msq, const EvtVector3R& p) {
    for (size_t i = 0; i < 3; ++i) msq += p.get(i)*p.get(i);
    return std::sqrt(msq);
}

EvtVector4R EvtGenInterface::initMomentum() const {
    static std::mt19937 gen{(*rd)()};
    static std::normal_distribution<> d{1, 0};

    const EvtVector3R electron_momentum = c_ideal_electron_momentum +
        m_energy_spread*d(gen) * random_unit_vector3d();
    const EvtVector3R positron_momentum = c_ideal_positron_momentum +
        m_energy_spread*d(gen) * random_unit_vector3d();

    static const double mElec = EvtPDL::getMass(EvtId(11, 11)) * 0.001;
    static const double mElecSq = mElec*mElec;
    
    const double eEl = energy(mElecSq, electron_momentum);
    const double ePo = energy(mElecSq, positron_momentum);
    const EvtVector3R total_momentum = electron_momentum + positron_momentum;

    debug() << "p(e-): ("
            << electron_momentum.get(0) << ", "
            << electron_momentum.get(1) << ", "
            << electron_momentum.get(2) << ")"  << endmsg;

    debug() << "p(e+): ("
            << positron_momentum.get(0) << ", "
            << positron_momentum.get(1) << ", "
            << positron_momentum.get(2) << ")"  << endmsg;

    debug() << "vpho momentum: "
            << eEl+ePo << ", "
            << total_momentum.get(0) << ", "
            << total_momentum.get(1) << ", "
            << total_momentum.get(2) << ")" << endmsg;

    return {eEl+ePo,
        total_momentum.get(0),
        total_momentum.get(1),
        total_momentum.get(2)};
}

StatusCode EvtGenInterface::getNextEvent(HepMC::GenEvent& theEvent) {
    EvtVector4R pInit = initMomentum();
    auto* parent = EvtParticleFactory::particleFactory(m_rootParticle, pInit);
    parent->setVectorSpinDensity();
    m_evtgen->generateDecay(parent);  // Generate the event and
    EvtHepMCEvent evt;                // Write out the results
    evt.constructEvent(parent);
    theEvent = *evt.getEvent();
    return StatusCode::SUCCESS;
}
