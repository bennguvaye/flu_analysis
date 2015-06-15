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

pars_file = sys.argv[1]
vals_file = sys.argv[2]

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

la, pa = np.zeros_like(ia), np.zeros([np.shape(ia)[0], np.shape(ia)[1], 3])
it = np.nditer([ia, ja, la],
               op_flags=[['readonly'], ['readonly'], ['writeonly']])

for i, j, l in it :
  ind = np.where(np.logical_and(vals[:, 0] == i, vals[:, 1] == j))[0]
  l[...] = vals[ind, 2]
  # p[...] = vals[ind, 3:6]

plt.pcolormesh(xa, ya, la, cmap=color_map)
plt.show()

