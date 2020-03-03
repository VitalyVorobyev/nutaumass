#! /usr/bin/env python

# from ROOT import gSystem
# gSystem.Load('libpodio.so')
# gSystem.Load('libpodioDict.so')
# gSystem.Load('libDataModel.so')
# gSystem.Load('libDataModelDict.so')

from EventStore import EventStore
import numpy as np
import pandas as pd

class PodioReader(object):
    """ Read sct-edm and convert to pandas DataFrame """
    def __init__(self, fname):
        """ Constructor """
        self.fname = fname
        self.__todf()

    def __genPclInfo(self, gp):
        """ """
        return [gp.charge(), gp.pdgId(), gp.p4().mass, gp.p4().px, gp.p4().py, gp.p4().pz, gp.startVertex().id() % 100]

    def __genVtxInfo(self, gv):
        """ """
        return [gv.x(), gv.y(), gv.z(), gv.ctau(), gv.id() % 100]

    def __todf(self):
        """ """
        store = EventStore(self.fname)
        pdtype = [('ch', int), ('id', int), ('m', float), ('px', float), ('py', float), ('pz', float), ('vtxid', int)]
        vdtype = [('x', float), ('y', float), ('z', float), ('ctau', float), ('id', int)]
        data = []
        print('Reading sctedm...')
        for idx, evt in enumerate(store):
            if idx % 10000 == 0:
                print('{} events'.format(idx))
            data.append([np.array([tuple(self.__genPclInfo(gp)) for gp in evt.get('allGenParticles')], dtype=pdtype),
                         np.array([tuple(self.__genVtxInfo(gv)) for gv in evt.get('allGenVertices')],  dtype=vdtype)])
        data = np.array(data)
        self.data = pd.DataFrame(dict(zip(['pdata', 'vdata'], [data[:, 0], data[:, 1]])))
        print('{} events in data set'.format(self.data.shape[0]))

def main():
    """ Unit test """
    # fname = 'tau3pi_10Mev_zero_spread_mass_10MeV.root'
    fname = 'tau3pi_10Mev_zero_spread.root'
    pr = PodioReader(fname)
    pr.data.to_pickle(fname.split('.')[0] + '.pkl')
#    pr = PodioReader('tau5piPhsp.root')
#    pr.data.to_pickle('tau5piPhsp.pkl')
#    events = pd.read_csv('tau3pi.csv')
#    events.to_pickle('tau3pi.pkl')
#    print(events['pdata'][0])

if __name__ == '__main__':
    main()
