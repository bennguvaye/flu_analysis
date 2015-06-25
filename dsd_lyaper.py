#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import sys

full_t_ser = stdin_to_array()
t_ser = cut_transient(365 * 100, full_t_ser)
#t_ser = full_t_ser
t = t_ser[:,0]
h = t_ser[:,1]
x = t_ser[:,2:14]
dx = t_ser[:,14:26]
jp = det_jump_points(dx)
l0 = lyap_exp(t, h, dx, jp)
per = compute_period(t, x)

to_be_written = str(l0) + ", " + \
                str(per[0]) + ", " + \
                str(per[1]) + ", " + \
                str(per[2]) + ", " + \
                str(per[3]) + ", " + \
                str(per[4]) + ", " + \
                str(per[5]) + ", " + \
                str(per[6]) + ", " + \
                str(per[7]) + ", " + \
                str(per[8]) + ", " + \
                str(per[9]) + ", " + \
                str(per[10]) + ", " + \
                str(per[11]) + "\n"

sys.stdout.write(to_be_written)
