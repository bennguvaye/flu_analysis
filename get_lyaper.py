#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import sys
import argparse
import matplotlib.pyplot as plt

full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 100, full_t_ser)
n = (np.shape(t_ser)[1] - 2) // 2 # normally necessarily an integer
#print("n", n)
t = t_ser[:, 0]
h = t_ser[:, 1]
x = t_ser[:, 2 : n + 2]
diff_x = x[1:] - x[:-1] # differentiated time series
diff_t = t[1:]
dx = t_ser[:, n + 2 : 2 * n + 2]
jp = det_jump_points(dx)
l0 = lyap_exp(t, h, dx, jp)
perconf = compute_period(t, x)
diff_perconf = compute_period(diff_t, diff_x)

dperconf = np.append(perconf, diff_perconf, axis=0)
lperconf = list(dperconf.flatten())

to_be_written = ("".join(["{}, "] * (4 * n + 1))[:-2] + "\n").format(l0, *lperconf)
# [:-2] : the last character is a ", " and we don't want it (empty field)
sys.stdout.write(to_be_written) 
