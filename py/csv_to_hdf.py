#!/usr/bin/env python3
import pandas as pd

path = '/home/vitaly'
for f in ['tau3pi', 'tau5piPhsp']:
    data = pd.read_csv(f'{path}/{f}.csv')
    print(data.columns)
    print(data['pdata'][0])
    data.to_hdf(f'{f}.h5', key='events', mode='w')
