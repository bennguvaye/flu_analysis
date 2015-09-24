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

"""
This script reads data from the file data_tseries.csv
and plots the corresponding time series and attractors.
"""

def pca_2(emb) :
  """Principal Component Analysis function that returns an array."""
  pcaer = skd.PCA(n_components=2)
  pca = pcaer.fit_transform(emb)
  
  return pca

def plot_tseries(*args, **kwargs) :
  """Simple plotting function to pass to FacetGrid."""
  data = kwargs.pop('data')
  return data.dropna().plot(x=args[0], y=args[1], **kwargs)

def plot_tseries_index(*args, **kwargs) :
  """Simple plotting function (plot against index) to pass to FacetGrid."""
  data = kwargs.pop('data')
  return data.dropna().plot(y=args[0], **kwargs)
  

# location of the data file
root_path = "/home/queue/Documents/2015stage/data"

# The data file is read in as a Pandas dataframe
data = pd.read_csv(root_path + "/sim_tseries.csv")
                   #parse_dates=[0])
data['filtered'] = False
tdata = data
tdata['t'] = tdata['t'] / 365.
#tdata = tdata[(tdata['t'] > '1950') & (tdata['t'] < '2016')]
tdata = tdata[(tdata['t'] > 100) & (tdata['t'] < 150)]

# Create (empty) dataframe to store PCA data in
data_pca = pd.DataFrame(columns=("origin", "pc1", "pc2"))

origs = ['ssd', 'sss', 'dsd', 'assd']
lags = [7, 7, 7, 7]
titles = ["(a)", 
          "(b)", 
          "(c)", 
          "(d)"] 

for orig, lag in zip(origs, lags) :
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  # embedding
  emb = lp.embedd(ts.values, 13, lag)
  # PCA
  pca = pca_2(emb)
  dfpca = pd.DataFrame(pca, columns=("pc1", "pc2"))
  dfpca['origin'] = orig
  # Add PCA data to dataframe
  data_pca = data_pca.merge(dfpca, how='outer')

f0 = plt.figure()
# layout
grid = gs.GridSpec(4, 10)
tmin = tdata['t'].min()
tmax = tdata['t'].max()
for i, (orig, titre) in enumerate(zip(origs, titles)) :
  # plot time series
  a0 = plt.subplot(grid[i, 0:8])
  p0 = tdata[(tdata['origin'] == orig)]\
        .plot('t', 'I_like', 
              ax=a0,
              xlim=[tmin, tmax])
  if i < 3 :
    a0.set_xlabel("")
    a0.set_xticklabels([])
  # print the "(a)", "(b)", etc...
  a0.set_ylabel(titre, 
                rotation='horizontal', 
                position=(-1., 1.05),
                size="large",
                weight="demi")
  #a0.set_title(titre, loc="left")

  # plot attractor
  a1 = plt.subplot(grid[i, 8:])
  data1 = data_pca[data_pca['origin'] == orig]
  p1 = data1.plot('pc1', 'pc2', 
                 ax=a1,
                 xlim=[data1.loc[:, 'pc1'].min(), data1.loc[:, 'pc1'].max()],
                 ylim=[data1.loc[:, 'pc2'].min(), data1.loc[:, 'pc2'].max()])
  if i < 3 :
    a1.set_xlabel("")
  a1.set_xticklabels([])
  a1.set_yticklabels([])

f0.savefig("/home/queue/Documents/2015stage/plots/sim_tseries.png", dpi=300)
#plt.show()
