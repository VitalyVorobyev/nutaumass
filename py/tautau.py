import os
from Configurables import ApplicationMgr

from Gaudi.Configuration import *
from Configurables import GenAlg, EvtGenInterface
from Configurables import HepMCToEDMConverter
from Configurables import PodioOutput
from Configurables import ScTauDataSvc
from Configurables import FlatSmearVertex
from GaudiKernel import SystemOfUnits as units

from PathResolver import PathResolver

import logging
from GaudiKernel.ProcessJobOptions import (InstallRootLoggingHandler, GetConsoleHandler)


_prefix = '<Py:GenTools> '
_level = logging.INFO

InstallRootLoggingHandler(prefix = _prefix, level = _level, with_time = False)
GetConsoleHandler(prefix = _prefix, with_time = False)

_root_logger = logging.getLogger()


decfile = 'tau-3prong-massive.dec'
mtau = 1.77682
ip = [.0, .0, .0]
nevt = 10**5
root = 'vpho'
ecms = 2*mtau + 0.01
espread = 0.
ofile = 'tau3pi_10Mev_zero_spread_mass_10MeV.root'

# Interaction point size (mm)
_root_logger.info('Uniform vertex smearing: {}'.format(ip))
_root_logger.info('Decay file: {}'.format(decfile))

# Vertex smearing
smeartool = FlatSmearVertex("VertexSmearingTool")
smeartool.xVertexMin = -ip[0]*units.mm
smeartool.xVertexMax =  ip[0]*units.mm
smeartool.yVertexMin = -ip[1]*units.mm
smeartool.yVertexMax =  ip[1]*units.mm
smeartool.zVertexMin = -ip[2]*units.mm
smeartool.zVertexMax =  ip[2]*units.mm

## Data service
podioevent = ScTauDataSvc("EventDataSvc")

# EvtGen
evtgen = EvtGenInterface('SignalProvider')
evtgen.userdec = decfile
evtgen.rootParticle = root
evtgen.Ecms = ecms
evtgen.Espred = 0.001 * espread
evtgen.evtpdl = '/home/vvorob/work/run/evt_massive_nutau.pdl'

gen = GenAlg('EvtGenAlg', SignalProvider=evtgen)
gen.hepmc.Path = 'hepmc'

out = PodioOutput('out', filename=ofile)
out.outputCommands = ["keep *"]

hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.genparticles.Path="allGenParticles"
hepmc_converter.genvertices.Path="allGenVertices"

options= {
    'TopAlg' : [gen, hepmc_converter, out],
    'EvtSel' : 'NONE',
    'ExtSvc' : [podioevent],
    'EvtMax' : nevt,
    'StatusCodeCheck' : True,
    'AuditAlgorithms' : True,
    'AuditTools' : True,
    'AuditServices' : True,
    'OutputLevel' : INFO,
}
ApplicationMgr(**options)
