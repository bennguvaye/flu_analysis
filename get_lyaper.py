#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import sys
import argparse
import matplotlib.pyplot as plt

info, full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 100, full_t_ser)
n = info['n'] // 2 # normally necessarily an integer
m = info['m']
#print("n", n)
#t = t_ser['t'].values
#h = t_ser['h'].values
t = t_ser['t']
h = t_ser['h']
t_ser_vals = t_ser.view((float, len(t_ser.dtype.names)))
x = t_ser_vals[:, 2 + m : n + 2 + m]
diff_x = x[1:] - x[:-1] # differentiated time series
diff_t = t[1:]
dx = t_ser_vals[:, n + 2 + m :]
jp = det_jump_points(dx)
l0 = lyap_exp(t, h, dx, jp)
perconf = compute_period(t, x)
diff_perconf = compute_period(diff_t, diff_x)

dperconf = np.append(perconf, diff_perconf, axis=0)
lperconf = list(dperconf.flatten())

to_be_written = ("".join(["{}, "] * (4 * n + 1))[:-2] + "\n").format(l0, *lperconf)
# [:-2] : the last character is a ", " and we don't want it (empty field)
sys.stdout.write(to_be_written) 
