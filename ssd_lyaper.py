#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import sys

t_ser = stdin_to_array()
t = t_ser[:,0]
h = t_ser[:,1]
x = t_ser[:,2:5]
dx = t_ser[:,5:8]
jp = det_jump_points(dx)
l0 = lyap_exp(t, h, dx, jp)
per = compute_period(t, x)

to_be_written = str(l0) + ", " + str(per[0]) + ", " + str(per[1]) + ", " + str(per[2]) + "\n"

sys.stdout.write(to_be_written)
