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

def hongkong_date_parser(chaine) :
  return pd.to_datetime(chaine.split(" - ")[0].split(" to ")[0], format="%d/%m/%Y")

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

hongkong = pd.read_csv(root_path + "/hong_kong_ili.csv",
                       sep=",",
                       na_values="",
                       parse_dates=[0],
                       date_parser=hongkong_date_parser)

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

hongkong['I_like'] = hongkong['ILIplus.total']
hongkong['origin'] = 'hongkong'
hongkong['type'] = 'ILI'

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

hongkong['new_t'] = hongkong['date']

iceland = iceland.dropna()
usa = usa.dropna()

df_l = [idf, isra, iceland, usa, hongkong]
data = pd.concat(df_l, join="inner")
#data = data.set_index('t')
data = data.rename(columns={'new_t':'t'})
data = data.set_index('t')
data = data.sort_index()
data = data[data.index < "2015"]
data.to_csv(root_path + "/data_tseries.csv")
