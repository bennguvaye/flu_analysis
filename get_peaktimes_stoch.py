#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster
"""
This script reads a time series csv from stdin and looks for the peaks
in the data.
The data should span longer than 50 years (the first fifty years are discarded).
In its current form, it is only adapted to use with the output of sim_ssd.
It can be easily adapted to use with other deterministic simulations
(just change x)


It then writes to stdout the mean distance between peaks and the values of the
peaks it found.

"""

from lyaper import *
import numpy
import sys
import argparse
import matplotlib.pyplot as plt

info, full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 1, full_t_ser)
n = info['n']
m = info['m']
t = t_ser[:, 0]
x = t_ser[:, m + 1 : n + m + 1]

t_p, x_p, lr, low, high = find_peaks_noise(56, t, x[:, 1:2]) # for sss
#t_p, x_p = find_peaks_det(t, x[:, 1:2])

print(t_p)

f = plt.figure()
a0 = f.add_subplot(211)
a0.plot(t, x[:, 1], "-g")
a0.plot(t_p[0], x_p[0], ".y")
a0.plot(t[low[0]], x[:, 1:2][low], ".r")
a0.plot(t[high[0]], x[:, 1:2][high], ".b")
a1 = f.add_subplot(212)
a1.plot(t, lr)

plt.show()

interpeak = t_p[1:] - t_p[:-1]
per = np.mean(interpeak)

approx_x_p = np.round(x_p, decimals=1)
peak_vals = np.unique(approx_x_p) 

l = len(peak_vals)

to_be_written = ("".join(["{}, "] * (l + 1))[:-2] + "\n").format(per, *peak_vals)
# [:-2] : the last characters are ", " and we don't want it (empty field)
sys.stdout.write(to_be_written) 
