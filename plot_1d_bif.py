#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots a one-dimensional bifurcation plot,
with values simulated by the deterministic model and the corresponding 
stochastic model.

"""

import sys
from math import log
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb
import csv

color_map = cm.cubehelix

root_path = sys.argv[1]

pars_file = root_path + "_pars.csv"
vals_file = root_path + "_vals.csv"
x_file = root_path + "_x.csv"
peak_file = root_path + "_peaks.csv"
per_file = root_path + "_per.csv"

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
print(len(vals))

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
a0 = f0.add_subplot(211)
a0.set_title("Peak incidence values")

a1 = f0.add_subplot(212)
a1.set_title("Period")

with open(peak_file, "w") as peak_fich :
  with open(per_file, "w") as per_fich :
    peak_wr = csv.writer(peak_fich)
    per_wr = csv.writer(per_fich)
    for i, j, x in it :
      ind = np.where(np.logical_and(vals_ij[:, 0] == i, vals_ij[:, 1] == j))[0]
      if len(ind) < 1 :
        print(i, j)
        pass
      else :
        if len(ind) > 1 :
          print(ind)
          ind = ind[0]
        n = len(vals[ind]) - 1
        loginc = [ log(1 + v) for v in vals[ind][1:] ]
        period = vals[ind][0] / 365
        a0.plot([x] * n, loginc, "r,")
        a1.plot([x], period, "b,")
        peak_wr.writerow(loginc)
        per_wr.writerow([period])

plt.show()

np.savetxt(x_file, xa, delimiter=",")

