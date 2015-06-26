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

t = t_ser[:,0] / 365
h = t_ser[:,1]
x = t_ser[:,2:14]

n = np.sum(x, axis=1)
s = np.sum(x[:, 0:3], axis=1)
i = np.sum(x[:, 6:10], axis=1)
q = np.sum(x[:, 10:14], axis=1)
r = x[:, 3]

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot(t, n)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, q, "g")
ax2.plot(t, r, "y")

plt.show()
