#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import numpy as np
import matplotlib.pyplot as plt
import sys

info, full_t_ser = stdin_to_array()

#t_ser = cut_transient(365 * 100, full_t_ser)
t_ser = full_t_ser

t = t_ser['t'] / 365
h = t_ser['h']
inc = t_ser['inc']
x = t_ser.loc[:, 'S':'R']
dx = t_ser.loc[:, 'dS':'dR']

n_hosts = x.sum(axis=1)
s = x['S']
i = x['I']
r = x['R']

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot(t, n_hosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, r, "y")

f3 = plt.figure()
ax3 = f3.add_subplot(111)
ax3.plot(t, inc, color="black")

f4 = plt.figure()
ax4 = f4.add_subplot(111)
for i in range(3) :
  ax4.plot(t, dx.values[:, i])

plt.show()
