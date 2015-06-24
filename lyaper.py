#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

# FIXME change the shebang on the cluster

import numpy as np
import sys
import fileinput

def rfftfreq(n, d=1.0):
  """
  Return the Discrete Fourier Transform sample frequencies
  (for usage with rfft, irfft).
  The returned float array `f` contains the frequency bin centers in cycles
  per unit of the sample spacing (with zero at the start). For instance, if
  the sample spacing is in seconds, then the frequency unit is cycles/second.
  Given a window length `n` and a sample spacing `d`::
  f = [0, 1, ..., n/2-1, n/2] / (d*n) if n is even
  f = [0, 1, ..., (n-1)/2-1, (n-1)/2] / (d*n) if n is odd
  Unlike `fftfreq` (but like `scipy.fftpack.rfftfreq`)
  the Nyquist frequency component is considered to be positive.
  Parameters
  ----------
  n : int
  Window length.
  d : scalar, optional
  Sample spacing (inverse of the sampling rate). Defaults to 1.
  Returns
  -------
  f : ndarray
  Array of length ``n//2 + 1`` containing the sample frequencies.
  Examples
  --------
  """
  if not isinstance(n, int):
    raise ValueError("n should be an integer")
  val = 1.0/(n*d)
  N = n//2 + 1
  results = np.arange(0, N, dtype=int)
  return results * val

def stdin_to_array() :
  """
  Reads a csv file from stdin. 

  """
  a = np.genfromtxt(fileinput.input(mode='rb'), delimiter=",", skip_header=1)
  return a

def compute_period(t, x) :
  """
  Returns the periods of the system.

  """
  n = len(t)
  centered_sys = x - np.mean(x, axis=0)
  sampling_spacing = (t[-1] - t[0]) / (n * 365)
  freqs = rfftfreq(n, sampling_spacing) 
  abs_ft = np.abs( np.fft.rfft(centered_sys, axis=0) )
  max_indices = np.argmax(abs_ft, axis=0)
  max_freqs = freqs[ max_indices ]
  
  return 1 / max_freqs

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

# function that determines jump points in dS, dI, dR
def det_jump_points(dx) :
  """
  Finds indices in the time series where the 2 norm of the variation jumps.a

  """
  l = np.shape(dx)[0]
  nds = norm2(dx)  # norm of variations # check that norm2 does what we want
  diffds = nds[1:] / nds[:-1]
  delt = np.mean(diffds)  # average variation variation
  ind = np.arange(l)
  jp = ind[(diffds < delt / 4)]  # check this syntax

  return jp

# compute lyapunov exponent
# time must be in years
def lyap_exp(t, h, dx, jp) :
  """
  Computes the maximal lyapunov exponent of the system.
  
  """
  ljp = len(jp)
  l0 = 0
  if ljp == 0 :
    l0 = l0 + np.log(norm2(dx[-1]) / norm2(dx[0]))
  else :
    l0 = l0 \
         + np.log(norm2(dx[-1]) / norm2(dx[jp[ljp - 1] + 1])) \
         + np.log(norm2(dx[jp[0]]) / norm2(dx[0]))
  if ljp > 1 :
    for i in range(len(jp) - 1) :
      l0 = l0 \
           + np.log(norm2(dx[jp[i + 1]]) / norm2(dx[jp[i] + 1]))
  tf = (t[-1] - t[0] - sum(h[jp])) / 365
  l0 = l0 / tf 

  return l0
