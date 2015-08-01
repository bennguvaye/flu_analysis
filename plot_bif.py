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

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sb

#color_map = cm.cubehelix
color_map = sb.cubehelix_palette(start=0.1, 
                                 rot=0.8, 
                                 gamma=1.2, 
                                 light=0.85,
                                 dark=0.15,
                                 as_cmap=True)
color_map.set_under(color='white')
color_map.set_over(color='black')

# The script takes one argument, the "root_path" to the input files.
# It will also be used as path for the output files.
root_path = sys.argv[1]

# Input files
pars_file = root_path + "_pars.csv"
vals_file = root_path + "_vals.csv"
# Output files
x_file = root_path + "_x.csv"
y_file = root_path + "_y.csv"
lambd_file = root_path + "_l0.csv"
p1_file = root_path + "_p1.csv"
p2_file = root_path + "_p2.csv"
p3_file = root_path + "_p3.csv"
p4_file = root_path + "_p4.csv"

pars = np.genfromtxt(pars_file, delimiter=",")
vals = np.genfromtxt(vals_file, delimiter=",")

if (np.shape(vals)[1] - 3) % 4 != 0 :
  
  raise ValueError("The input is not as expected : wrong size of lines, "
                   + str(np.shape(vals)[1]))
n = (np.shape(vals)[1] - 3) // 4 # number of dim of the system

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
  try :
    i[...] = pars[ind, 0]
    j[...] = pars[ind, 1]
  except ValueError :
    print(x, y)
    print(ind)
    print(pars[ind])
    raise

# Five initially identical arrays 
la, p_cntr_peak_a, p_cntr_force_a, p_diff_peak_a, p_diff_force_a = \
  np.zeros_like(ia), np.zeros_like(ia), np.zeros_like(ia), np.zeros_like(ia), np.zeros_like(ia)
# Iteration over all the 2d arrays in the same order
it = np.nditer([ia, ja, la, p_cntr_peak_a, p_cntr_force_a, 
                            p_diff_peak_a, p_diff_force_a],
               op_flags=[['readonly'], ['readonly'], 
                         ['writeonly'], ['writeonly'], ['writeonly'],
                                        ['writeonly'], ['writeonly']],
               order='C')

for i, j, l, p1, p2, p3, p4 in it :
  ind = np.where(np.logical_and(vals[:, 0] == i, vals[:, 1] == j))[0]
  try :
    l[...] = vals[ind, 2]
    # the component with the highest period is what we take
    # (one non-stationary component makes the whole system non-stationary)
    p1[...] = np.max(vals[ind, 3 + 0 * n : 3 + 1 * n])
    # the component with the least signal portion around 1 is taken
    p2[...] = np.min(vals[ind, 3 + 1 * n : 3 + 2 * n])
    p3[...] = np.max(vals[ind, 3 + 2 * n : 3 + 3 * n])
    p4[...] = np.min(vals[ind, 3 + 3 * n : 3 + 4 * n])
    
  except ValueError : 
    pass

# Saving to output files
for fname, ar in zip([x_file, y_file, lambd_file, 
                      p1_file, p2_file, p3_file, p4_file],
                     [xa, ya, la, 
                      p_cntr_peak_a, p_cntr_force_a, p_diff_peak_a, p_diff_force_a]) :
  np.savetxt(fname, ar, delimiter=",")

# Careful : In some cases we can get bad values (-inf, inf, nan) in the array
# We'd like them to have a special value
fin_cntr_peak = p_cntr_peak_a[np.isfinite(p_cntr_peak_a)]
fin_cntr_force = p_cntr_peak_a[np.isfinite(p_cntr_force_a)]
fin_diff_peak = p_cntr_peak_a[np.isfinite(p_diff_peak_a)]
fin_diff_force = p_cntr_peak_a[np.isfinite(p_diff_force_a)]

# Plotting the results
f1 = plt.figure()
a1 = f1.add_subplot(111)
a1.set_title("Lyapunov exponent")
p1 =a1.pcolormesh(xa, ya, la, cmap=color_map)
plt.colorbar(p1)

f2 = plt.figure()
a2 = f2.add_subplot(111)
a2.set_title("Period as measured by max peak of centered time series")
p2 = a2.pcolormesh(xa, ya, p_cntr_peak_a, 
                   cmap=color_map, 
                   vmin=fin_cntr_peak.min(),
                   vmax=fin_cntr_peak.max())
plt.colorbar(p2, extend='both')

f3 = plt.figure()
a3 = f3.add_subplot(111)
a3.set_title("Period as measured by signal strength around 1 of centered time series")
p3 = a3.pcolormesh(xa, ya, p_cntr_force_a, 
                   cmap=color_map,
                   vmin=fin_cntr_force.min(),
                   vmax=fin_cntr_force.max())
plt.colorbar(p3, extend='both')

f4 = plt.figure()
a4 = f4.add_subplot(111)
a4.set_title("Period as measured by max peak of differentiated time series")
p4 = a4.pcolormesh(xa, ya, p_diff_peak_a, 
                   cmap=color_map, 
                   vmin=fin_diff_peak.min(),
                   vmax=fin_diff_peak.max())
plt.colorbar(p4, extend='both')

f5 = plt.figure()
a5 = f5.add_subplot(111)
a5.set_title("Period as measured by signal strength around 1 of differentiated time series")
p5 = a5.pcolormesh(xa, ya, p_diff_force_a, 
                   cmap=color_map, 
                   vmin=fin_diff_force.min(),
                   vmax=fin_diff_force.max())
plt.colorbar(p5, extend='both')

plt.show()

