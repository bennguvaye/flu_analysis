#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import numpy as np
import scipy.signal as scs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

import lyaper as lp

def plot_tseries(*args, **kwargs) :
  data = kwargs.pop('data')
  return data.dropna().plot(x=args[0], y=args[1], **kwargs)

def plot_tseries_index(*args, **kwargs) :
  data = kwargs.pop('data')
  return data.dropna().plot(y=args[0], **kwargs)
  

#root_path = sys.argv[1]
root_path = "/home/queue/Documents/2015stage/data"

data = pd.read_csv(root_path + "/tseries.csv",
                   parse_dates=[0])
data['filtered'] = False
tdata = data
tdata = tdata[(tdata['t'] > '1930') & (tdata['t'] < '2016')]


firco = scs.firwin(numtaps=5, cutoff=1/3, window="hamming")
for orig in ['idf', 'israel', 'iceland', 'usa'] :
  typ = np.unique(tdata[tdata['origin'] == orig]['type'])
  if typ.shape[0] > 1 :
    raise ValueError("several types for one origin !")
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  ind = tdata[tdata['origin'] == orig].dropna()['t']
  fts = scs.lfilter(firco, 1., ts)
  
  rdf = pd.DataFrame(np.transpose(np.array([ind, fts])), columns=["t", "I_like"])
  rdf['origin'] = orig
  rdf['type'] = typ[0]
  rdf['filtered'] = True
  tdata = tdata.merge(rdf, how='outer')
  
tdata = tdata.set_index('t')

sub = tdata[(tdata['origin'] == 'idf') 
          | (tdata['origin'] == 'usa')
          | (tdata['origin'] == 'iceland')
          | (tdata['origin'] == 'israel')]

g = sb.FacetGrid(sub, row="filtered", col="origin")
g.map_dataframe(plot_tseries_index, "I_like", sharey=False)

plt.show()

data_pca = pd.DataFrame(columns=("origin", "pc1", "pc2"))

origs = ['ssd', 'sss', 'dsd', 'dss', 'idf', 'israel', 'usa', 'iceland']
lags = [7, 7, 7, 7, 1, 2, 1, 1]

for orig, lag in zip(origs, lags) :
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  emb = lp.embedd(ts.values, 13, lag)
  pca = lp.pca_2(emb)
  dfpca = pd.DataFrame(pca, columns=("pc1", "pc2"))
  dfpca['origin'] = orig
  data_pca = data_pca.merge(dfpca, how='outer')

g0 = sb.FacetGrid(tdata, col="origin", col_wrap=4, sharey=False)
g0.map_dataframe(plot_tseries_index, "I_like")

g1 = sb.FacetGrid(data_pca, col="origin", col_wrap=4, sharex=False, sharey=False)
g1.map(plt.plot, "pc1", "pc2")

plt.show()
