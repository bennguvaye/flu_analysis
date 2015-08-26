
#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots a one-dimensional bifurcation plot,
with values simulated by the deterministic model and the corresponding 
stochastic model.

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

color_map = cm.cubehelix

root_path = sys.argv[1]

pars_file = root_path + "_pars.csv"
vals_file = root_path + "_vals.csv"
x_file = root_path + "_x.csv"

pars = np.genfromtxt(pars_file, delimiter=",")
vals_ij = np.genfromtxt(vals_file, delimiter=",", usecols=(0,1))
vals = list()

def convert_row(row) :
  return [ float(v) for i, v in enumerate(row) if i >= 2 ]

with open(vals_file, 'r') as fich :
  liseur = csv.reader(fich, delimiter=",")
  for row in liseur :
    vals.append(convert_row(row))
#vals = np.genfromtxt(vals_file, delimiter=",")

pars = pars[1:]

xa = np.sort(np.unique(pars[:,2]))

ia, ja = np.zeros_like(xa), np.zeros_like(xa)

it = np.nditer([xa, ia, ja], 
               op_flags=[['readonly'], ['writeonly'], ['writeonly']])

for x, i, j in it :  
  ind = np.where(pars[:, 2] == x)[0]
  i[...] = pars[ind, 0]
  j[...] = pars[ind, 1]


it = np.nditer([ia, ja, xa], 
               op_flags=[['readonly'], ['readonly'], ['readonly']]) 

f0 = plt.figure()
a0 = f0.add_subplot(111)
a0.set_title("Peak incidence values")

for i, j, x in it :
  ind = np.where(np.logical_and(vals_ij[:, 0] == i, vals_ij[:, 1] == j))[0]
  try :
    n = len(vals[ind]) - 1
    a0.plot([x] * n, vals[ind][1:], "r,")
  except TypeError :
    print(ind)
    raise
  except ValueError : 
    pass

#f1 = plt.figure()
#a1 = f1.add_subplot(111)
#a1.set_title("Lyapunov exponent")
#p1 =a1.pcolormesh(xa, ya, la, cmap=color_map)
#plt.colorbar(p1)
#
#f2 = plt.figure()
#a2 = f2.add_subplot(111)
#a2.set_title("Period as measured by max peak of centered time series")
#p2 =a2.pcolormesh(xa, ya, p_cntr_peak_a, cmap=color_map)
#plt.colorbar(p2)
#
#f3 = plt.figure()
#a3 = f3.add_subplot(111)
#a3.set_title("Period as measured by peak size around 1 of centered time series")
#p3 = a3.pcolormesh(xa, ya, p_cntr_force_a, cmap=color_map)
#plt.colorbar(p3)
#
#f4 = plt.figure()
#a4 = f4.add_subplot(111)
#a4.set_title("Period as measured by max peak of differentiated time series")
#p4 = a4.pcolormesh(xa, ya, p_diff_peak_a, cmap=color_map)
#plt.colorbar(p4)
#
#f5 = plt.figure()
#a5 = f5.add_subplot(111)
#a5.set_title("Period as measured by peak size around 1 of differentiated time series")
#p5 = a5.pcolormesh(xa, ya, p_diff_force_a, cmap=color_map)
#plt.colorbar(p5)

plt.show()

