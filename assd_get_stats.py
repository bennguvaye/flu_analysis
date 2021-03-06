#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster
# we assume the number of age classes m is 3

from lyaper import *
from stdin_with_pandas import stdin_to_array
import numpy as np
import matplotlib.pyplot as plt
import sys

info, full_t_ser = stdin_to_array()

#t_ser = cut_transient(365 * 100, full_t_ser)
t_ser = full_t_ser

t = t_ser['t'] / 365
h = t_ser['h']
inc = t_ser['inc']

n = info['n'] // 2
m = info['m']

a = n // 3

print("n :", n)
print("a :", a)

x = t_ser.iloc[:, 2 + m : n + 2 + m]
dx = t_ser.iloc[:, n + 2 + m :]

n_hosts = np.sum(x, axis=1)
n_dhosts = np.sum(dx, axis=1)

jp = det_jump_points(dx)

s = np.sum(x.iloc[:, 0 : a], axis=1)
i = np.sum(x.iloc[:, a : 2 * a], axis=1)
r = np.sum(x.iloc[:, 2 * a : 3 * a], axis=1)

f1 = plt.figure()
ax0 = f1.add_subplot(211)
ax0.plot(t, n_hosts)
ax1 = f1.add_subplot(212)
ax1.plot(t, n_dhosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s)
ax2.plot(t, i)
ax2.plot(t, r)

f3 = plt.figure()
ax31 = f3.add_subplot(111)
ax31.plot(t, inc)

#f3 = plt.figure()
#ax3 = f3.add_subplot(111)
#for i in range(a) :
#  ax3.plot(t, x[:, a + i])

f4 = plt.figure()
ax4 = f4.add_subplot(111)
for i in range(3) :
  for k in range(a) :
    if i == 0 :
      c = "red"
    elif i == 1 :
      c = "blue"
    else :
      c = "green"
    ax4.plot(t, dx.iloc[:, a * i + k], c)
ax4.plot(t[jp], np.zeros_like(t[jp]), 'o')

plt.show()
