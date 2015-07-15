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

full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 50, full_t_ser)
n = (np.shape(t_ser)[1] - 2) // 2 # normally necessarily an integer
t = t_ser[:, 0]
h = t_ser[:, 1]
x = t_ser[:, 2 : n + 2]

t_p, x_p = find_peaks_det(t, x[:, 1:2]) # for ssd

interpeak = t_p[1:] - t_p[:-1]
per = np.mean(interpeak)

peak_vals = np.unique(x_p) 

l = len(peak_vals)

to_be_written = ("".join(["{}, "] * (l + 1))[:-2] + "\n").format(per, *peak_vals)
# [:-2] : the last characters are ", " and we don't want it (empty field)
sys.stdout.write(to_be_written) 
