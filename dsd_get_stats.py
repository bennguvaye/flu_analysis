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
inc1 = t_ser['inc1']
inc2 = t_ser['inc2']
x = t_ser.loc[:, 'R0':'Q12']
dx = t_ser.loc[:, 'dR0':'dQ12']

n_hosts = x.sum(axis=1)
dn_hosts = dx.sum(axis=1)
s = x.loc[:, 'R0':'R2'].sum(axis=1)
i = x.loc[:, 'I10':'I21'].sum(axis=1)
q = x.loc[:, 'Q0':'Q12'].sum(axis=1)
r = x.loc[:, 'R12']

jp = det_jump_points(dx)

f1 = plt.figure()
ax0 = f1.add_subplot(211)
ax0.plot(t, n_hosts)
ax1 = f1.add_subplot(212)
ax1.plot(t, dn_hosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, q, "g")
ax2.plot(t, r, "y")

f3 = plt.figure()
ax31 = f3.add_subplot(211)
ax31.plot(t, inc1)
ax32 = f3.add_subplot(212)
ax32.plot(t, inc2)

f4 = plt.figure()
ax4 = f4.add_subplot(111)
for i in range(12) :
  ax4.plot(t, dx.iloc[:, i])
ax4.plot(t[jp], np.zeros_like(t[jp]), 'o')

plt.show()
