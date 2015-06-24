#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script does two things :
-- Build the arrays X, Y, C necessary for pcolormesh, from two csv files
containing containing the parameter values and the simulation results
indexed by i (process number on the cluster) 
and j (command number in the process)

-- Plot the arrays ? Save them ? Save the plot ?

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

color_map = cm.cubehelix

root_path = sys.argv[1]

pars_file = root_path + "_pars.csv"
vals_file = root_path + "_vals.csv"
x_file = root_path + "_x.csv"
y_file = root_path + "_y.csv"
lambd_file = root_path + "_l0.csv"
per_file = root_path + "_per.csv"

pars = np.genfromtxt(pars_file, delimiter=",")
vals = np.genfromtxt(vals_file, delimiter=",")


# for pars : we need to drop the first line ("i", "j", "x", "y") (converted silently to nans)
pars = pars[1:]
x = np.sort(np.unique(pars[:,2]))
y = np.sort(np.unique(pars[:,3]))

xa, ya = np.meshgrid(x, y)

print(np.shape(xa))
print(np.shape(ya))

ia, ja = np.zeros_like(xa), np.zeros_like(ya)

it = np.nditer([xa, ya, ia, ja], 
               op_flags=[['readonly'], ['readonly'], ['writeonly'], ['writeonly']])

for x, y, i, j in it :  
  ind = np.where(np.logical_and(pars[:, 2] == x, pars[:,3] == y))[0]
  i[...] = pars[ind, 0]
  j[...] = pars[ind, 1]


la, pa = np.zeros_like(ia), \
         np.zeros([np.shape(vals[:, 3:])[1], 
                   np.shape(ia)[0], 
                   np.shape(ia)[1]])
it = np.nditer([ia, ja, la, pa],
               flags=['reduce_ok'],
               op_flags=[['readonly'], ['readonly'], 
                         ['readwrite'], ['writeonly']],
               op_axes=[[-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [0, 1, 2]])

for i, j, l, p in it :
  ind = np.where(np.logical_and(vals[:, 0] == i, vals[:, 1] == j))[0]
  try :
    l[...] = vals[ind, 2]
    #p[...] = vals[ind, 3:]
  except ValueError : 
    pass

for fname, ar in zip([x_file, y_file, lambd_file],
                     [xa, ya, la]) :
  np.savetxt(fname, ar, delimiter=",")

plt.pcolormesh(xa, ya, la, cmap=color_map)
plt.colorbar()
plt.show()

