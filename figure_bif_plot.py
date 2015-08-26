#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
"Recent" version of the script :
Four measures of periodicity are expected.

This script does two things :
-- Build the arrays X, Y, C necessary for pcolormesh, from two csv files
containing containing the parameter values and the simulation results
indexed by i (process number on the cluster) 
and j (command number in the process)
-- save the various C arrays corresponding to max lyapunov exponent and 
several measures of periodicity.
-- plot the "pcolormeshes" (5 of them)


"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gs
import seaborn as sb

#color_map = cm.cubehelix
color_map_l0 = sb.cubehelix_palette(start=0.1, 
                                 rot=0.9, 
                                 gamma=1.2, 
                                 light=0.85,
                                 dark=0.15,
                                 as_cmap=True)
color_map_l0.set_under(color='white')
color_map_l0.set_over(color='black')

# have two different colorbars, for lambda0 and periods ?
color_map_p = sb.cubehelix_palette(start=0.1, 
                                 rot=1.5, 
                                 gamma=1.2, 
                                 light=0.9,
                                 dark=0.1,
                                 as_cmap=True)
color_map_p.set_under(color='white')
color_map_p.set_over(color='black')

# The script takes one argument, the "root_path" to the input files.
# It will also be used as path for the output files.
root_path = "/home/queue/Documents/2015stage/data/"
names = ['ssd_etaNg_10000', 'dsd_etaNg_10000_new', 
         'assd_etaNg_10000_R03', 'adsd_etaNg_10000']
n = len(names)
X, Y, L0, P = list(), list(), list(), list()

grid = gs.GridSpec(n, 20)

for i, name in enumerate(names) :
  # Output files
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

titles = ['ssd', 'dsd', 'assd', 'adsd']

for i, (tit, x, y, l0, p) in enumerate(zip(titles, X, Y, L0, P)) :
  a0 = plt.subplot(grid[i, :8])
  p0 = a0.pcolormesh(x, y, l0, 
                     cmap=color_map_l0,
                     vmin=vmin_l0,
                     vmax=vmax_l0)
  #a0.set_title(name + "_l0")
  a0.set_ylabel(tit)
  if i < 3 : 
    a0.set_xticklabels([])
                
  a1 = plt.subplot(grid[i, 10:18])
  p1 = a1.pcolormesh(x, y, p,
                     cmap=color_map_p,
                     vmin=vmin_p,
                     vmax=vmax_p)
  #a1.set_title(name + "_p3")
  if i < 3 :
    a1.set_xticklabels([])

plt.colorbar(p0, cax=plt.subplot(grid[:, 8]), use_gridspec=True)
plt.colorbar(p1, cax=plt.subplot(grid[:, 18]), use_gridspec=True)

## Careful : In some cases we can get bad values (-inf, inf, nan) in the array
## We'd like them to have a special value
#fin_cntr_peak = p_cntr_peak_a[np.isfinite(p_cntr_peak_a)]
#fin_cntr_force = p_cntr_peak_a[np.isfinite(p_cntr_force_a)]
#fin_diff_peak = p_cntr_peak_a[np.isfinite(p_diff_peak_a)]
#fin_diff_force = p_cntr_peak_a[np.isfinite(p_diff_force_a)]

plt.show()

