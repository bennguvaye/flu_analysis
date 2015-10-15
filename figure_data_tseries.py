#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

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
data = pd.read_csv(root_path + "/data_tseries.csv",
                   parse_dates=[0])
data['filtered'] = False
tdata = data
# We only keep part of the time series.
tdata = tdata[(tdata['t'] > '1950') & (tdata['t'] < '2016')]

# We filter the data
## create the filter
firco = scs.firwin(numtaps=5, cutoff=1/3, window="hamming")
for orig in ['idf', 'israel', 'iceland', 'usa', 'hongkong'] :
  typ = np.unique(tdata[tdata['origin'] == orig]['type'])
  if typ.shape[0] > 1 :
    raise ValueError("several types for one origin !")
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  ind = tdata[tdata['origin'] == orig].dropna()['t']
  # apply filter
  fts = scs.lfilter(firco, 1., ts)
  
  rdf = pd.DataFrame(np.transpose(np.array([ind, fts])), columns=["t", "I_like"])
  rdf['origin'] = orig
  rdf['type'] = typ[0]
  rdf['filtered'] = True
  # add the filtered data to our dataframe
  tdata = tdata.merge(rdf, how='outer')
  
# Create (empty) dataframe to store PCA data in
data_pca = pd.DataFrame(columns=("origin", "pc1", "pc2"))

#origs = ['idf', 'israel', 'usa', 'iceland', 'hongkong']
#lags = [1, 3, 1, 1, 1]
#titles = ["(a)", 
#          "(b)", 
#          "(c)", 
#          "(d)", 
#          "(e)"] 

# We don't plot for usa and iceland
origs = ['idf', 'israel', 'hongkong']
lags = [1, 3, 1]
titles = ["(a)",
          "(b)",
          "(c)"]

for orig, lag in zip(origs, lags) :
  ts = tdata[tdata['origin'] == orig].dropna()['I_like']
  # Embed in high dimension
  emb = lp.embedd(ts.values, 13, lag)
  # Keep the first two components
  pca = pca_2(emb)
  # As a dataframe
  dfpca = pd.DataFrame(pca, columns=("pc1", "pc2"))
  dfpca['origin'] = orig
  # Add the PCA data to our PCA dataframe
  data_pca = data_pca.merge(dfpca, how='outer')

f0 = plt.figure()
# figure layout
grid = gs.GridSpec(3, 10)
# idf starts the earliest after usa/iceland
tmin = tdata[tdata['origin']=='idf']['t'].min()
tmax = tdata['t'].max()

for i, (orig, titre) in enumerate(zip(origs, titles)) :
  # plot the time series
  a0 = plt.subplot(grid[i, 0:8])
  p0 = tdata[(tdata['origin'] == orig) & (tdata['filtered'])]\
        .plot('t', 'I_like', 
              ax=a0,
              xlim=[tmin, tmax])
  # plot the "(a)", "(b)", etc...
  a0.set_ylabel(titre, 
                rotation='horizontal', 
                size="large",
                weight="demi",
                position=(-0.5,1.05))
  #a0.set_title(titre, loc="left")

  # plot the PCA
  a1 = plt.subplot(grid[i, 8:])
  data1 = data_pca[data_pca['origin'] == orig]
  p1 = data1.plot('pc1', 'pc2', 
                 ax=a1,
                 xlim=[data1.loc[:, 'pc1'].min(), data1.loc[:, 'pc1'].max()],
                 ylim=[data1.loc[:, 'pc2'].min(), data1.loc[:, 'pc2'].max()])

  a1.set_xticklabels([])
  a1.set_yticklabels([])
  
  if i < 4 :
    a0.set_xlabel("")
    a0.set_xticklabels([])
    a1.set_xlabel("")
    #a1.set_xticklabels([])

f0.savefig("/home/queue/Documents/2015stage/plots/data_tseries.png", dpi=300)
#plt.show()
