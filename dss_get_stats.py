#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

from lyaper import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import sys

info, full_t_ser = stdin_to_array()

#t_ser = cut_transient(365 * 100, full_t_ser)
t_ser = full_t_ser

#print("t_ser")
#print(t_ser.head())

t = t_ser['t'] / 365
inc1 = t_ser['inc1']
inc2 = t_ser['inc2']
x = t_ser.loc[:, 'R0':'Q12']

#print("t")
#print(t.head())
#print("x")
#print(x.head())

n_hosts = x.sum(axis=1)
s = x.loc[:, 'R0':'R2'].sum(axis=1)
i = x.loc[:, 'I10':'I21'].sum(axis=1)
q = x.loc[:, 'Q0':'Q12'].sum(axis=1)
r = x.loc[:, 'R12']

f1 = plt.figure()
ax0 = f1.add_subplot(211)
ax0.plot(t, n_hosts)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(t, s, "r")
ax2.plot(t, i, "b")
ax2.plot(t, q, "g")
ax2.plot(t, r, "y")

f3 = plt.figure()
ax31 = f3.add_subplot(111)
ax31.plot(t, x.loc[:, 'Q0'])
ax31.plot(t, x.loc[:, 'Q1'])
ax31.plot(t, x.loc[:, 'Q2'])
ax31.plot(t, x.loc[:, 'Q12'])

f4 = plt.figure()
ax41 = f4.add_subplot(211)
ax41.plot(t, inc1)
ax42 = f4.add_subplot(212)
ax42.plot(t, inc2)

plt.show()
