#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import numpy as np
import matplotlib.pyplot as plt
import sys

full_t_ser = stdin_to_array()

#t_ser = cut_transient(365 * 100, full_t_ser)
t_ser = full_t_ser

t = t_ser[:, 0] / 365
h = t_ser[:, 1]
x = t_ser[:, 2:14]
dx = t_ser[:, 14:]

n = np.sum(x, axis=1)
dn = np.sum(dx, axis=1)
s = np.sum(x[:, 0:3], axis=1)
i = np.sum(x[:, 6:10], axis=1)
q = np.sum(x[:, 10:14], axis=1)
r = x[:, 3]

jp = det_jump_points(dx)

f1 = plt.figure()
ax0 = f1.add_subplot(211)
ax0.plot(t, n)
ax1 = f1.add_subplot(212)
ax1.plot(t, dn)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, q, "g")
ax2.plot(t, r, "y")

f3 = plt.figure()
ax3 = f3.add_subplot(111)
for i in range(12) :
  ax3.plot(t, dx[:, i])
ax3.plot(t[jp], np.zeros_like(t[jp]), 'o')

plt.show()
