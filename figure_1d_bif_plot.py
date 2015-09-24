#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots a figure with multiple 1d bifurcation diagrams.
The data that is read corresponds to files output by plot_1d_bif.py

"""

import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gs
import seaborn as sb

root_path = "/home/queue/Documents/2015stage/data/"
# will be plotted on the first column
names_0 = [('ssd_etaN_5000', 'sss_etaN_5000'), 
           ('dsd_etaN_1000', 'dss_etaN_1000')]
# will be plotted on the second column
names_1 = [('ssd_g_5000', 'sss_g_5000'),
           ('dsd_g_1000', 'dss_g_1000')]
n = len(names_0) # must be equal to len(names_1)
X, P = list(), list()

titles = [["(a)", "(b)"], ["(c)", "(d)"]]

f0 = plt.figure()
grid = gs.GridSpec(n, 2)
for j, names in enumerate([names_0, names_1]) :
  # for each column
  for i, (det_name, stoch_name) in enumerate(names) :
    # for each row
    a0 = plt.subplot(grid[i, j])
    # Input files
    print(i)
    x_file = root_path + det_name + "_x.csv"
    det_pk_file = root_path + det_name + "_peaks.csv"
    stoch_pk_file = root_path + stoch_name + "_peaks.csv"
    det_per_file = root_path + det_name + "_per.csv"
    stoch_per_file = root_path + stoch_name + "_per.csv"
  
    X = np.genfromtxt(x_file, delimiter=",")
    det_per = np.genfromtxt(det_per_file, delimiter=",")
    stoch_per = np.genfromtxt(stoch_per_file, delimiter=",")
    with open(det_pk_file, 'r') as det_fich :
      with open(stoch_pk_file, 'r') as stoch_fich :
        det_rd = csv.reader(det_fich)
        stoch_rd = csv.reader(stoch_fich)
        # read lines from the det file and stoch file at once
        for x, det_loginc, stoch_loginc in zip(X, det_rd, stoch_rd) :
          det_n = len(det_loginc)
          stoch_n = len(stoch_loginc)
          try :
            # plot the stochastic data
            a0.plot([x] * stoch_n, stoch_loginc, 
                    ",", color=sb.xkcd_rgb["medium green"], alpha=0.5)
          except ValueError : # missing value
            print(stoch_loginc, stoch_n)
            raise
          # plot the deterministic data
          a0.plot([x] * det_n, det_loginc, 
                  ",", color=sb.xkcd_rgb["pale red"], alpha=0.5)
    a0.set_ylabel(titles[j][i],
                  rotation="horizontal", 
                  position=(-1., 1.05), 
                  size="large",
                  weight="demi")
    if i < 1 : 
      a0.set_xticklabels([])
                  

#  a1.plot(X, stoch_per, 
#          ",", color=sb.xkcd_rgb["medium green"], alpha=0.5)
#  a1.plot(X, det_per,
#          ",", color=sb.xkcd_rgb["pale red"], alpha=0.5)


f0.savefig("/home/queue/Documents/2015stage/plots/one_dim_bif.png", dpi=300)
#plt.show()

