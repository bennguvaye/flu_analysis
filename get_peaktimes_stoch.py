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
t_ser = cut_transient(365 * 100, full_t_ser)
# n = info['n'] // 2 # tmp
n = info['n']
m = info['m']
t = t_ser['t']
try :
  inc = t_ser['inc']
except ValueError :
  inc = t_ser['inc1'] + t_ser['inc2']
t_ser_vals = t_ser.view((float, len(t_ser.dtype.names)))
#x = t_ser[:, m + 1 : n + m + 1]

t_p, x_p, lr, low, high, maxi, sel = find_peaks_noise(61, t, inc) # for sss

#print("lowhighmaxisel")
#print(low)
#print(low[0].shape)
#print(high)
#print(high[0].shape)
#print(maxi)
#print(maxi.shape)
#print(sel[:200])

#t_yr = t / 365
#
#f = plt.figure()
#a0 = f.add_subplot(211)
#a0.plot(t_yr, inc, "-g")
##a0.plot(t_p, x_p, ".y")
#a0.plot(t_yr[maxi], inc[maxi], ".y")
#a0.plot(t_yr[low[0]], inc[low], ".r")
#a0.plot(t_yr[high[0]], inc[high], ".b")
#a1 = f.add_subplot(212)
#a1.plot(t_yr, lr)
#
#plt.show()

interpeak = t_p[1:] - t_p[:-1]
#per = np.mean(interpeak)

approx_x_p = np.round(x_p, decimals=1)
peak_vals = np.unique(approx_x_p) 

l_1 = len(interpeak)
l_2 = len(peak_vals)

to_be_written_1 = ("".join(["{}, "] * l_1)[:-2] + "//").format(*interpeak)
# [:-2] : the last characters are ", " and we don't want it (empty field)
to_be_written_2 = ("".join(["{}, "] * l_2)[:-2] + "\n").format(*peak_vals)

sys.stdout.write(to_be_written_1) 
sys.stdout.write(to_be_written_2) 
