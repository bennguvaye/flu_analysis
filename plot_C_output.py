#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots interesting data about the output from the full simulation
C program.

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

color_map = cm.cubehelix

root_path = sys.argv[1]
C_prog_arg = sys.argv[2]

strain_0_file = root_path + "/" + C_prog_arg + "/J0.0." + C_prog_arg
strain_1_file = root_path + "/" + C_prog_arg + "/J1.0." + C_prog_arg
Nc_file = "/home/queue/Documents/2015stage/code/C/data/N.dat"

strain_0 = np.genfromtxt(strain_0_file, delimiter="\t")
strain_1 = np.genfromtxt(strain_1_file, delimiter="\t")
Nca = np.genfromtxt(Nc_file)

n = np.shape(strain_0)[0]
dt = 0.25 # see in pandemics.h
prntime = 56 # see in pandemics.h

t = np.linspace(0, n * dt * prntime / 365, n)

# we cut the transient (first 2 years)
strain_0 = strain_0[np.where(t > 0)] / Nca[np.newaxis, :] * 100000
strain_1 = strain_1[np.where(t > 0)] / Nca[np.newaxis, :] * 100000
t = t[np.where(t > 0)]

print(np.shape(t))
print(np.shape(strain_0))
print(np.shape(strain_1))

# we start by plotting the aggregated (on cities) data for both strains
c0 = 237 
n0 = "New-York"
c1 = 256
n1 = "Washington"
c2 = 137 
n2 = "Mexico"
c3 = 0  
n3 = "Buenos Aires"
c4 = 163 
n4 = "Singapour"
c5 = 9 
n5 = "Sydney"
c6 = 67
n6 = "Havane"
c7 = 3
n7 = "Cairns"

cl = [c0, c1, c2, c3, c4, c5, c6, c7]
nl = [n0, n1, n2, n3, n4, n5, n6, n7]
ic = list()
for i in range(8) :
  ic.append([strain_0[:, cl[i]], strain_1[:, cl[i]], strain_0[:, cl[i]] + strain_1[:, cl[i]]])

i0 = np.sum(strain_0, axis=1)
i1 = np.sum(strain_1, axis=1)

#f1 = plt.figure()
#a1 = f1.add_subplot(111)
#p1 = a1.plot(t, i0)
#p2 = a1.plot(t, i1)

# we can also plot the time series as a pcolormesh. Why not.
c = np.arange(260)
# TODO arranger les villes dans un ordre bien selon la location géographique
# on voit pas des tonnes les deux phases...
# aussi faire les deux souches indépendamment pour voir si ya quelque chose à voir

#f2 = plt.figure()
#a2 = f2.add_subplot(111)
#p3 = a2.pcolormesh(t, c, np.transpose(strain_0 + strain_1), cmap=color_map)
#plt.colorbar(p3)

cols = ["blue", "red", "black"]
for i in range(8) :
  f = plt.figure()
  a = f.add_subplot(111)
  for j in range(3) :
    a.plot(t, ic[i][j], cols[j])
  a.set_title(nl[i])

plt.show()
#
#
#it = np.nditer([ia, ja, la, p_cntr_peak_a, p_cntr_force_a, 
#                            p_diff_peak_a, p_diff_force_a],
#               op_flags=[['readonly'], ['readonly'], 
#                         ['writeonly'], ['writeonly'], ['writeonly'],
#                                        ['writeonly'], ['writeonly']],
#               op_axes=[[-1, 0, 1], [-1, 0, 1], 
#                        [-1, 0, 1], [-1, 0, 1], [-1, 0, 1], 
#                                    [-1, 0, 1], [-1, 0, 1]])
#for i, j, l, p1, p2, p3, p4 in it :
#  ind = np.where(np.logical_and(vals[:, 0] == i, vals[:, 1] == j))[0]
#  try :
#    l[...] = vals[ind, 2]
#    p1[...] = np.max(vals[ind, 2 + 0 * n : 2 + 1 * n])
#    p2[...] = np.min(vals[ind, 2 + 1 * n : 2 + 2 * n])
#    p3[...] = np.max(vals[ind, 2 + 2 * n : 2 + 3 * n])
#    p4[...] = np.max(vals[ind, 2 + 3 * n : 2 + 4 * n])
#    
#  except ValueError : 
#    pass
#
#for fname, ar in zip([x_file, y_file, lambd_file],
#                     [xa, ya, la]) :
#  np.savetxt(fname, ar, delimiter=",")
#
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
#
#plt.show()
#
