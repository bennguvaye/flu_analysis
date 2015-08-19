#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sys

def stdin_to_array() :
  """
  Reads a csv file from stdin. 

  """
  strinfo = sys.stdin.readline()
  [strn, strm] = strinfo.split(",")
  info = {'n':int(strn.split("=")[1]), 'm':int(strm.split("=")[1])}
  data = pd.read_csv(sys.stdin)

  return info, data

