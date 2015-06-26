#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster
# we assume the number of age classes m is 3

from lyaper import *
import numpy as np
import matplotlib.pyplot as plt
import sys

full_t_ser = stdin_to_array()

#t_ser = cut_transient(365 * 100, full_t_ser)
t_ser = full_t_ser

t = t_ser[:, 0] / 365
h = t_ser[:, 1]
n = (np.shape(t_ser)[1] - 2) / 2 # normally necessarily an integer
m = n / 3
x = t_ser[:, 2 : n + 2]

n_hosts = np.sum(x, axis=1)

s = np.sum(x[:, 0 : m], axis=1)
i = np.sum(x[:, m : 2 * m], axis=1)
r = np.sum(x[:, 2 * m : 3 * m], axis=1)

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot(t, n_hosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, r, "y")

plt.show()
