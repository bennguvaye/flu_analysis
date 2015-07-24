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

def cut_transient(t_end_transient, t_ser) :
  """
  Cut part of a time series out (from time 0 to time t_end_transient)
  
  """
  inds_sel = np.where(t_ser[:,0] > t_end_transient)
  new_t_ser = t_ser[inds_sel]
  
  return new_t_ser

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
  
  periods_by_max = 1 / max_freqs
  
  confidence = np.mean(abs_ft[np.where(np.logical_and(freqs > 0.8, freqs < 1.2))],
                      axis=0) \
               / np.mean(abs_ft, axis=0)

  return np.append(periods_by_max[np.newaxis, :], 
                   confidence[np.newaxis, :], 
                   axis=0)

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

  Returns :
  - jp : the jump indices

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

def find_peaks_det(t, x) :
  """
  Find peaks in the data by looking at the differentiated serie.  

  Parameters :
  - t : Float array. The time series.
  - x : Float 2D array. The dependent variables.
  Returns :
  - t_peaks : the times of peaks
  - x_peaks : the values of peaks

  """
  n = np.shape(t)[0]
  k = np.shape(x)[1]
  
  diff_x = x[1:] - x[:-1]
  pos = np.where(diff_x > 0)
  neg = np.where(diff_x < 0)
  
  peaks = np.where(
          np.logical_and(
          np.roll(diff_x, shift=1, axis=0)[:-1] > 0, diff_x[:-1] < 0
          )
          )
  
  t_peaks = t[peaks[0]]
  x_peaks = x[peaks]

  return t_peaks, x_peaks


def find_peaks_noise(win, t, x) :
  """
  Find peaks in the data via moving polynomial regression  

  Parameters :
  - win : Float. The time window over which to regress.
  - t : Float array. The time series.
  - x : Float 2D array. The dependent variables.
  Returns :
  - t_peaks : the times of peaks
  - x_peaks : the values of peaks
  - lr : the likelihood ratios

  """
  # Fit a 2nd degree polynomial on a window of like 1 month
  # Actually we want to do all this only on the I data right ?
  # So we're only passing the I data in x
  n = np.shape(t)[0]
  k = np.shape(x)[1]
  print("k", k)
  print("n", n)
  t_peaks = [list()] * k
  x_peaks = [list()] * k
  ends = np.zeros( [n, k] )
  lra = np.zeros( [n, k] )
  sel = np.zeros( [n, k] )
  l01a = np.zeros( [n, 2, k] )
  tl = list()
  x0l = list()
  x1l = list()

  for i, ti in enumerate(t) :
    start = i
    try :
      end = np.where(t > ti + win)[0][0] # first index that passes the window
    except IndexError :
      # we've reached the last window
      break
    ends[i] = end
    twin, xwin = t[start:end], x[start:end, :]
    p0, res0, _, _, _ = np.polyfit(twin, xwin, 1, full=True)
    p1, res1, _, _, _ = np.polyfit(twin, xwin, 2, full=True)

    sig0 = np.sqrt(res0 / (end - start))
    sig1 = np.sqrt(res1 / (end - start))

    # need to repeat t so that dimensiosn are ok
    twin_r = np.repeat(twin[:, np.newaxis], k, axis=1)
    l0a = 1 / (np.sqrt(2 * np.pi) * sig0) \
          * np.exp(- (xwin - p0[0] * twin_r - p0[1]) ** 2 / (2 * sig0 ** 2))
    l1a = 1 / (np.sqrt(2 * np.pi) * sig1) \
          * np.exp(- (xwin - p1[0] * twin_r ** 2 - p1[1] * twin_r - p1[2]) ** 2 / (2 * sig1 ** 2))   # likelihood ratio array
    # compute the statistic
    
    l0 = np.prod(l0a, axis=0)
    l1 = np.prod(l1a, axis=0)
    lr = -2 * np.sum(np.log(l0a) - np.log(l1a), axis=0)
    # with a type 1 error of 1 % : compare to 6.64
    maxi = np.argmax(xwin, axis=0)
    tmax = twin_r[maxi]
    xmax = xwin[maxi]
    #sel_polyfit = np.logical_and(lr > 6.64, p1[0] < 0)
    sel_polyfit = np.logical_and(lr > 100, p1[0] < 0)
    lra[i] = lr
    sel[i] = sel_polyfit
    l01a[i, 0] = l0
    l01a[i, 1] = l1
    tl.append(twin)
    x0l.append(p0[0] * twin + p0[1])
    x1l.append(p1[0] * twin ** 2 + p1[1] * twin + p1[2])
  lows = np.where(np.logical_and(sel[:-1], 
                        np.logical_not(np.roll(sel, shift=-1, axis=0)[:-1])))
  highs = np.where(np.logical_and(np.logical_not(sel[:-1]), 
                         np.roll(sel, shift=-1, axis=0)[:-1]))
  highs = (ends[highs].astype(int), highs[1])
  # problem : has to work if k > 1
  maxi = np.array([
              np.argmax(x[l0:h0, j], axis=0) for (l0, h0, l1, h1) 
                in zip(lows[0], highs[0], lows[1], highs[1])
                 ])

  #t_peaks = [ np.append(l, tmax[j]) if selection[j] else l for j, l in enumerate(t_peaks) ]
  #x_peaks = [ np.append(l, xmax[j]) if selection[j] else l for j, l in enumerate(x_peaks) ]
    # pas mal mais il vaut mieux se baser sur des points successifs ayant le fit
    # et prendre que un point là-dessus ?

  return t_peaks, x_peaks, lra, lows, highs#, l01a, tl, x0l, x1l
