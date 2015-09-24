#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots a figure with multiple 2d bifurcation diagrams.
(with white in place of non UPCA regions)
The data that is read corresponds to files output by plot_bif.py

"""

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gs
import seaborn as sb

color_map_l0 = sb.cubehelix_palette(start=0.1, 
                                 rot=0.9, 
                                 gamma=1.2, 
                                 light=0.85,
                                 dark=0.15,
                                 as_cmap=True)
color_map_l0.set_bad(color='white')

color_map_p = sb.cubehelix_palette(start=0.1, 
                                 rot=1.5, 
                                 gamma=1.2, 
                                 light=0.9,
                                 dark=0.1,
                                 as_cmap=True)
color_map_p.set_under(color='white')
color_map_p.set_over(color='black')

root_path = "/home/queue/Documents/2015stage/data/"
names = ['ssd_etaNg_10000', 'dsd_etaNg_10000_new', 
         'assd_etaNg_10000_R03']
n = len(names)
X, Y, L0, P = list(), list(), list(), list()

for i, name in enumerate(names) :
  # Input files
  print(i)
  x_file = root_path + name + "_x.csv"
  y_file = root_path + name + "_y.csv"
  lambd_file = root_path + name + "_l0.csv"
  p3_file = root_path + name + "_p3.csv"
  per_file = root_path + name + "_per.csv"

  X.append( np.genfromtxt(x_file, delimiter=",") )
  Y.append( np.genfromtxt(y_file, delimiter=",") )
  L0.append( np.genfromtxt(lambd_file, delimiter=",") )
  try :
    P.append( np.genfromtxt(p3_file, delimiter=",") )
  except OSError :
    P.append( np.genfromtxt(per_file, delimiter=",") )

vmin_l0 = min([ np.min(a) for a in L0 ])
vmax_l0 = max([ np.max(a) for a in L0 ])

vmin_p = min([ np.min(a) for a in P ])
vmax_p = max([ np.max(a) for a in P ])

#titles = ['ssd', 'dsd', 'assd']
titles = ["(a)", "(b)", "(c)"]

f0 = plt.figure()
grid = gs.GridSpec(n, 10)
for i, (tit, x, y, l0, p) in enumerate(zip(titles, X, Y, L0, P)) :
  l0_upca = ma.array(l0.copy())
  l0 = ma.array(l0)
  l0_upca[~((0.9 < p) & (p < 1.1))] = ma.masked
  #l0[((0.7 < p) & (p < 1.3))] = ma.masked
  a0 = plt.subplot(grid[i, :8])
  p00 = a0.pcolormesh(x, y, l0_upca, 
                     cmap=color_map_l0,
                     alpha=1.,
                     edgecolors='face',
                     vmin=vmin_l0,
                     vmax=vmax_l0)
  a0.set_ylabel(tit, 
                rotation="horizontal", 
                position=(-1., 1.05), 
                size="large",
                weight="demi")
  if i < 2 : 
    a0.set_xticklabels([])

plt.colorbar(p00, cax=plt.subplot(grid[:, 8]), use_gridspec=True)

f0.savefig("/home/queue/Documents/2015stage/plots/two_dim_bif.png", dpi=300)
#plt.show()

