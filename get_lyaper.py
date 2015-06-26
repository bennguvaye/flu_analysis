#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import sys

full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 100, full_t_ser)
n = (np.shape(t_ser)[1] - 2) / 2 # normally necessarily an integer
t = t_ser[:, 0]
h = t_ser[:, 1]
x = t_ser[:, 2 : n + 2]
dx = t_ser[:, n + 2 : 2 * n + 2]
jp = det_jump_points(dx)
l0 = lyap_exp(t, h, dx, jp)
perconf = compute_period(t, x)

lperconf = list(perconf.flatten('F'))

to_be_written = ("".join(["{}, "] * (2 * n + 1))+"\n").format(l0, *lperconf)

sys.stdout.write(to_be_written)
