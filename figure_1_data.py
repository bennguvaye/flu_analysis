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

def idf_date_parser(chaine) :
  return pd.to_datetime(chaine, format="%Y%W")

def isra_date_parser(chaine) :
  return pd.to_datetime(chaine, format="%d-%b-%Y")

def icelusa_date_parser(chaine) :
  return pd.to_datetime(chaine, format="%m%Y")

#root_path = sys.argv[1]
root_path = "/home/queue/Documents/2015stage/data"

t = np.linspace(0, 35, 35 * 52)

idf = pd.read_csv(root_path + "/idf_data.csv", 
                  sep=",", 
                  na_values="-") 
#                  parse_dates=[0],
#                  date_parser=idf_date_parser)
isra = pd.read_csv(root_path + "/israel.csv", 
                   sep=" ",
                   parse_dates=[0],
                   date_parser=isra_date_parser)
icelusa = pd.read_csv(root_path + "/iceland_usa.csv", 
                      sep=" ", 
                      na_values="")
#                      parse_dates=[[0,1]],
#                      date_parser=icelusa_date_parser)

idf['I_like'] = idf['Ile-de-France']
idf['origin'] = 'idf'
idf['type'] = 'ILI'

isra['I_like'] = isra['ILI']
isra['origin'] = 'israel'
isra['type'] = 'ILI'

icelusa = pd.melt(icelusa,
                  id_vars=['month', 'year'],
                  value_vars=['ICELAND_', 'US_FLU_DEATHS'],
                  var_name='origin',
                  value_name='I_like')
iceland = icelusa[icelusa['origin'] == 'ICELAND_']
iceland['origin'] = 'iceland'
iceland['type'] = 'ILI'

usa = icelusa[icelusa['origin'] == 'US_FLU_DEATHS']  
usa['type'] = 'deaths'
usa['origin'] = 'usa'

# For the empirical parameter set
names = [ "ssd", "sss", "dsd", "dss" ]
fnames = [ root_path + trail for trail in 
           ["/ssd_105.csv", "/sss_108.csv", "/dsd_105.csv", "/dss_108.csv"] ]

data = {name:path_to_df(fname, name)[1] for name, fname in zip(names, fnames)}

idf['new_t'] = pd.date_range(pd.to_datetime("308-1984", format="%j-%Y"),
                             periods=idf.shape[0],
                             freq="W")
isra['new_t'] = isra['Date']

start_time = pd.datetime(iceland['year'][0], iceland['month'][0], 1) 
iceland['new_t'] = pd.date_range(start_time,
                                 periods=iceland.shape[0],
                                 freq="MS")
usa['new_t'] = pd.date_range(start_time,
                             periods=usa.shape[0],
                             freq="MS")
iceland = iceland.dropna()
usa = usa.dropna()

data['dsd']['inc'] = data['dsd']['inc1'] + data['dsd']['inc2']
data['dss']['inc'] = data['dss']['inc1'] + data['dss']['inc2']

for key, item in data.items() :
  item['new_t'] = pd.date_range(start_time,
                                periods=item.shape[0],
                                freq="D")
#                               freq="0.0027397260273972603Y")
  item['I_like'] = item['inc']
  item['origin'] = key
  item['type'] = 'inc'

df_l = list(data.values()) + [idf, isra, iceland, usa]
data = pd.concat(df_l, join="inner")
#data = data.set_index('t')
data = data.rename(columns={'new_t':'t'})
data = data.set_index('t')
data = data.sort_index()
data = data[data.index < "2015"]
data.to_csv(root_path + "/tseries.csv")
