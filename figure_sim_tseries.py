#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

#import sys
import numpy as np
import scipy.signal as scs
import sklearn.decomposition as skd
import pandas as pd
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
import seaborn as sb

import lyaper as lp

def pca_2(emb) :
  pcaer = skd.PCA(n_components=2)
  pca = pcaer.fit_transform(emb)
  
  return pca

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
tdata = tdata[(tdata['t'] > '1950') & (tdata['t'] < '2016')]

sub = tdata[(tdata['origin'] == 'ssd') 
          | (tdata['origin'] == 'sss')
          | (tdata['origin'] == 'dsd')
          | (tdata['origin'] == 'dss')]

data_pca = pd.DataFrame(columns=("origin", "pc1", "pc2"))

origs = ['ssd', 'sss', 'dsd', 'dss']
lags = [7, 7, 7, 7]

for orig, lag in zip(origs, lags) :
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  emb = lp.embedd(ts.values, 13, lag)
  #pca = lp.pca_2(emb)
  pca = pca_2(emb)
  dfpca = pd.DataFrame(pca, columns=("pc1", "pc2"))
  dfpca['origin'] = orig
  data_pca = data_pca.merge(dfpca, how='outer')

f0 = plt.figure()
grid = gs.GridSpec(4, 11)
tmin = tdata['t'].min()
tmax = tdata['t'].max()
for i, orig in enumerate(origs) :
  a0 = plt.subplot(grid[i, 0:8])
  p0 = tdata[(tdata['origin'] == orig)]\
        .plot('t', 'I_like', 
              ax=a0,
              xlim=[tmin, tmax])
  if i < 3 :
    a0.set_xlabel("")
    a0.set_xticklabels([])
  a0.set_ylabel(orig)

  a1 = plt.subplot(grid[i, 9:])
  data1 = data_pca[data_pca['origin'] == orig]
  p1 = data1.plot('pc1', 'pc2', 
                 ax=a1,
                 xlim=[data1.loc[:, 'pc1'].min(), data1.loc[:, 'pc1'].max()],
                 ylim=[data1.loc[:, 'pc2'].min(), data1.loc[:, 'pc2'].max()])

#g0 = sb.FacetGrid(tdata, col="origin", col_wrap=4, sharey=False)
#g0.map_dataframe(plot_tseries_index, "I_like")

#g1 = sb.FacetGrid(data_pca, ="origin", col_wrap=4, sharex=False, sharey=False)
#g1.map(plt.plot, "pc1", "pc2")
# FIXME problem : trend for usa...

plt.show()
