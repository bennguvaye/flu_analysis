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

#vals = vals[:,:-1]

if (np.shape(vals)[1] - 3) % 4 != 0 :
  raise ValueError("The input is not as expected : wrong size of lines")
n = (np.shape(vals)[1] - 3) // 4 # number of dim of the system

#if (np.shape(vals)[1] - 3) % 2 != 0 :
#  raise ValueError("The input is not as expected : wrong size of lines")
#n = (np.shape(vals)[1] - 3) // 2 # number of dim of the system

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


la, p_cntr_peak_a, p_cntr_force_a, p_diff_peak_a, p_diff_force_a = \
                                 [np.zeros_like(ia)]*5
it = np.nditer([ia, ja, la, p_cntr_peak_a, p_cntr_force_a, 
                            p_diff_peak_a, p_diff_force_a],
               op_flags=[['readonly'], ['readonly'], 
                         ['writeonly'], ['writeonly'], ['writeonly'],
                                        ['writeonly'], ['writeonly']],
               op_axes=[[-1, 0, 1], [-1, 0, 1], 
                        [-1, 0, 1], [-1, 0, 1], [-1, 0, 1], 
                                    [-1, 0, 1], [-1, 0, 1]])

#la, p_peak_a, p_force_a = \
#                                 [np.zeros_like(ia)]*3
#
#it = np.nditer([ia, ja, la, p_peak_a, p_force_a],
#               op_flags=[['readonly'], ['readonly'], 
#                         ['writeonly'], ['writeonly'], ['writeonly']],
#               op_axes=[[-1, 0, 1], [-1, 0, 1], 
#                        [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]) 

for i, j, l, p1, p2, p3, p4 in it :
#for i, j, l, p1, p2 in it :
  ind = np.where(np.logical_and(vals[:, 0] == i, vals[:, 1] == j))[0]
  try :
    l[...] = vals[ind, 2]
    p1[...] = np.max(vals[ind, 2 + 0 * n : 2 + 1 * n])
    p2[...] = np.min(vals[ind, 2 + 1 * n : 2 + 2 * n])
    p3[...] = np.max(vals[ind, 2 + 2 * n : 2 + 3 * n])
    p4[...] = np.max(vals[ind, 2 + 3 * n : 2 + 4 * n])
    
  except ValueError : 
    pass

for fname, ar in zip([x_file, y_file, lambd_file],
                     [xa, ya, la]) :
  np.savetxt(fname, ar, delimiter=",")

f1 = plt.figure()
a1 = f1.add_subplot(111)
a1.set_title("Lyapunov exponent")
p1 =a1.pcolormesh(xa, ya, la, cmap=color_map)
plt.colorbar(p1)

f2 = plt.figure()
a2 = f2.add_subplot(111)
a2.set_title("Period as measured by max peak of centered time series")
p2 =a2.pcolormesh(xa, ya, p_cntr_peak_a, cmap=color_map)
plt.colorbar(p2)

f3 = plt.figure()
a3 = f3.add_subplot(111)
a3.set_title("Period as measured by peak size around 1 of centered time series")
p3 = a3.pcolormesh(xa, ya, p_cntr_force_a, cmap=color_map)
plt.colorbar(p3)

f4 = plt.figure()
a4 = f4.add_subplot(111)
a4.set_title("Period as measured by max peak of differentiated time series")
p4 = a4.pcolormesh(xa, ya, p_diff_peak_a, cmap=color_map)
plt.colorbar(p4)

f5 = plt.figure()
a5 = f5.add_subplot(111)
a5.set_title("Period as measured by peak size around 1 of differentiated time series")
p5 = a5.pcolormesh(xa, ya, p_diff_force_a, cmap=color_map)
plt.colorbar(p5)

plt.show()

