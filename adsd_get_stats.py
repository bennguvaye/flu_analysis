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
n = (np.shape(t_ser)[1] - 2) // 2 # normally necessarily an integer
m = n // 12
print("n :", n)
print("m :", m)
x = t_ser[:, 2 : n + 2]
dx = t_ser[:, n + 2:]

n_points = np.shape(x)[0]
n_hosts = np.sum(x, axis=1)
n_dhosts = np.sum(dx, axis=1)

x = np.reshape(x, [n_points, 12, m])

s = np.sum(x[:, 0:3], axis=1)
i = np.sum(x[:, 6:10], axis=1)
q = np.sum(x[:, 10:14], axis=1)
r = x[:, 3]

jp = det_jump_points(dx)


f1 = plt.figure()
ax0 = f1.add_subplot(211)
ax0.plot(t, n_hosts)
ax1 = f1.add_subplot(212)
ax1.plot(t, n_dhosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, np.sum(s, axis=1))
ax2.plot(t, np.sum(i, axis=1))
ax2.plot(t, np.sum(r, axis=1))

f3 = plt.figure()
ax3 = f3.add_subplot(111)
for j in range(m) :
  ax3.plot(t, i[:, j])

f4 = plt.figure()
ax4 = f4.add_subplot(111)
for i in range(12) :
  for k in range(m) :
    if i in range(4) :
      c = "red"
    elif i in range(4, 8) :
      c = "blue"
    else :
      c = "green"
    ax4.plot(t, dx[:, m * i + k], c)
ax4.plot(t[jp], np.zeros_like(t[jp]), 'o')

plt.show()
