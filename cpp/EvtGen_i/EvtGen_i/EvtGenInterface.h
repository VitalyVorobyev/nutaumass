//
// Copyright (C) 2018-2019 BINP for the benefit of the SCTau collaboration
//
#pragma once
#define EVTGEN_CPP11

#include "GaudiKernel/ToolHandle.h"
#include "AuroraAlg/AuroraTool.h"

#include "GenInterfaces/IHepMCProviderTool.h"
#include "GenInterfaces/IEvtGenModel.h"

#include "EvtGenBase/EvtVector4R.hh"
#include "EvtGenBase/EvtVector3R.hh"
#include "EvtGenBase/EvtId.hh"

#include <memory>
#include <string>
#include <list>
#include <random>

// Forward HepMC
namespace HepMC {
    class GenEvent;
}

// Forward EvtGen
class EvtGen;
class EvtRandomEngine;
class EvtExternalGenList;
class EvtDecayBase;
class EvtMTRandomEngine;

class EvtGenInterface : public AuroraTool, virtual public IHepMCProviderTool {
    /** EvtGen engine */
    std::unique_ptr<EvtGen> m_evtgen;
    /** Random number engine */
    std::unique_ptr<EvtRandomEngine> m_rndm;
    /** Externals config */
    std::unique_ptr<EvtExternalGenList> m_genList;
    /** External decay models */
    std::list<EvtDecayBase*> m_exmodels;

    /** evt.pdl file */
    Gaudi::Property<std::string> m_evtpdl{this,
        "evtpdl", "EvtGen_i/evt.pdl", "The evt.pdl file"};
    /** DECAY.DEC file */
    Gaudi::Property<std::string> m_decdec{this,
        "decaydec", "EvtGen_i/DECAY.DEC", "The DECAY.DEC file"};
    /** User decay file */
    Gaudi::Property<std::string> m_usrdec{this,
        "userdec", "", "User decay file"};
    /** Root particle */
    Gaudi::Property<std::string> m_rootpcl{this,
        "rootParticle", "psi(3770)", "Root particle"};
    /** CM energy */
    Gaudi::Property<double> m_ecms{this,
        "Ecms", 0., "CM energy for non-resonance events (GeV)"};
    /** Energy spread */
    Gaudi::Property<double> m_energy_spread{this,
        "Espred", 0.001, "CM energy spread (GeV)"};
    /** Beam crossing angle */
    Gaudi::Property<double> m_angle{this,
        "angle", 30, "Beam crossing angle (mrad)"};
    /** Beam crossing angle spread */
    // Gaudi::Property<double> m_angle_spread{this,
        // "angle", 0, "Beam crossing angle spread (mrad)"};
    /** Seed for the random number generator */
    Gaudi::Property<unsigned int> m_rndm_seed{this,
        "RndmSeed", 0, "Seed for the random number generator (unsigned int)"};

//    ToolHandleArray<IEvtGenModel> m_addon_models{this};
  /// Handle to the tools saving the output
  /// to be replaced with the ToolHandleArray<IEvtGenModel>  m_addon_models{this}
    std::vector<IEvtGenModel*> m_addon_models;
  /// Names for the model tools
  /// to be deleted once the ToolHandleArray<IEvtGenModel> m_addon_models is in place
    Gaudi::Property<std::vector<std::string>> m_modelToolNames{this, "AddonModels", {}, "Additional models of decays"};

    // TODO: move the cross angle logic into separate tool
    StatusCode initKinematics();
    EvtVector4R initMomentum() const;
    EvtVector3R random_unit_vector3d() const;
    std::unique_ptr<std::random_device> rd;

    EvtVector3R c_ideal_electron_momentum;
    EvtVector3R c_ideal_positron_momentum;
    double m_energy;
    EvtId m_rootParticle;

 public:
    /** Constructor */
    EvtGenInterface(const std::string& type, const std::string& name,
                    const IInterface* parent);

    virtual StatusCode initialize() override final;
    virtual StatusCode finalize() override final;
    virtual StatusCode getNextEvent(HepMC::GenEvent& theEvent) override final;
};
