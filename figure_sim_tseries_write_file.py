#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

def path_to_df(path, orig) :
  """
  Reads a csv file from path
  
  """
  with open(path, 'r') as fich :
    strinfo = fich.readline()
    [strn, strm] = strinfo.split(",")
    info = {'n':int(strn.split("=")[1]), 'm':int(strm.split("=")[1])}
    data = pd.read_csv(fich, sep=",")
    data['origin'] = orig
  return info, data

#root_path = sys.argv[1]
root_path = "/home/queue/Documents/2015stage/data"


# For the empirical parameter set
names = [ "ssd", "sss", "dsd", "dss", "assd" ]
fnames = [ root_path + trail for trail in 
           ["/ssd_105.csv", 
            "/sss_108.csv", 
            "/dsd_105.csv", 
            "/dss_108.csv", 
            "/assd_105.csv"] ]

data = {name:path_to_df(fname, name)[1] for name, fname in zip(names, fnames)}

data['dsd']['inc'] = data['dsd']['inc1'] + data['dsd']['inc2']
data['dss']['inc'] = data['dss']['inc1'] + data['dss']['inc2']

start_time = pd.datetime(1890, 1, 1) 
for key, item in data.items() :
  #item['new_t'] = pd.date_range(start_time,
  #                              periods=item.shape[0],
  #                              freq="2D")
  item['I_like'] = item['inc']
  item['origin'] = key
  item['type'] = 'inc'

df_l = list(data.values())
data = pd.concat(df_l, join="inner")
#data = data.set_index('t')
#data = data[data['new_t'] < '2015']
#data = data.rename(columns={'t':'old_t', 'new_t':'t'})
data = data.set_index('t')
data = data.sort_index()
data.to_csv(root_path + "/sim_tseries.csv")
