#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

import numpy as np
import sys
import fileinput

def stdin_to_array() :
  """
  Reads a csv file from stdin. 

  """
  a = np.genfromtxt(fileinput.input(mode='rb'), delimiter=",", skip_header=1)
  return a

def cut_transient(t_end_transient, t_ser) :
  """
  Cut part of a time series out (from time 0 to time t_end_transient)
  
  """
  inds_sel = np.where(t_ser[:,0] > t_end_transient)
  new_t_ser = t_ser[inds_sel]
  
  return new_t_ser

def norm2(x) :
  """
  Compute the 2-norm along the last axis.

  """
  if len(np.shape(x)) > 1 :
    f = lambda y : np.inner(y,y)
    nsq = np.apply_along_axis(f, 1, x)
  else :
    nsq = np.inner(x,x)
  return np.sqrt(nsq)

# either the max in a moving window of one year
# and just uniq it
# or try to find the main changing points :
# how ?

