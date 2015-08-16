#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots interesting data about the output from the full simulation
C program.

"""

import sys
import numpy as np
import pandas as pd

#root_path = sys.argv[1]
#C_prog_arg = str(sys.argv[2])
#n_reps = int(sys.argv[3])

root_path = "/home/queue/Documents/2015stage/data/C_g_data"
n_reps = 10

cities = pd.read_csv("/home/queue/Documents/2015stage/code/C/data/140527_260villes2009plus2.dat", sep=";",
                     decimal=",")
transport = pd.read_csv("/home/queue/Documents/2015stage/code/C/data/260transport2009.dat", sep=";",
                     decimal=",")

Nc_file = "/home/queue/Documents/2015stage/code/C/data/N.dat"
g_file = "/home/queue/Documents/2015stage/data/C_g_10_pars.csv"
#eta_file = "/home/queue/Documents/2015stage/data/eta.csv"

Nca = np.genfromtxt(Nc_file)
g_df = pd.read_csv(g_file)

dt = 0.25 # see in pandemics.h
prntime = 56 # see in pandemics.h

def get_rep_data(C_prog_arg, rep) :
  strain_1_file = root_path + "/" + str(C_prog_arg) \
                + "/J0." + str(rep) + "." + str(C_prog_arg)
  strain_2_file = root_path + "/" + str(C_prog_arg) \
                + "/J1." + str(rep) + "." + str(C_prog_arg)
  
  newind = np.arange(260) + 1
  strain_1 = pd.read_csv(strain_1_file, 
                         sep="\t", 
                         header=None,
                         names=newind)
  strain_2 = pd.read_csv(strain_2_file, 
                         sep="\t",
                         header=None,
                         names=newind)
  n = np.shape(strain_1)[0]
  strain_1['strain'] = 1
  strain_2['strain'] = 2
  dates = pd.date_range(pd.datetime(1930, 1, 1),
                        periods=n,
                        freq="W") # FIXME lack robustness
  strain_1['t'] = dates
  strain_2['t'] = dates
  #strain_1['t'] = np.linspace(0, n * dt * prntime / 365, n)
  #strain_2['t'] = np.linspace(0, n * dt * prntime / 365, n)
  
  out = pd.merge(strain_1, strain_2, 
                 #on=('t', 'strain'),
                 how='outer')
  #out = pd.concat([strain_1, strain_2], axis=1)
  out['rep'] = rep

  out = pd.melt(out, 
                id_vars=['t', 'strain', 'rep'], 
                value_vars=list(newind),
                var_name="city_newind",
                value_name='inc')
  out.head() 
 
  return out

def get_g_data(g_ind) :
  out_l = [ get_rep_data(g_ind, rep) for rep in range(n_reps) ]
  df = pd.concat(out_l)
  df['g_ind'] = g_df['i'][g_ind] # 1/ * 365 ? 

  return df

out_l = [ get_g_data(g_ind) for g_ind in range(1) ] # FIXME change to 10 eventually
df = pd.concat(out_l)


by_zone = np.arange(260) + 1
idzone = cities.select(
           lambda s : (s == 'zone')
                      or (s == 'newid'),
           axis=1)

idzone = idzone.sort("zone")
idzone["by_zone"] = by_zone

idzone_from = idzone.rename_axis({'zone':'from_zone', 
                                  'newid':'from',
                                  'by_zone':'from_by_zone'},
                                 axis=1)
idzone_to = idzone.rename_axis({'zone':'to_zone', 
                                'newid':'to',
                                'by_zone':'to_by_zone'},
                               axis=1)

print(idzone_from.head())
print(idzone_to.head())

ntransp = pd.merge(left=transport,
                   right=idzone_from,
                   how='inner',
                   left_on='from',
                   right_on='from')

ntransp = pd.merge(left=ntransp,
                   right=idzone_to,
                   how='inner',
                   left_on='to',
                   right_on='to')

print("after merge")
print(ntransp.head())

#ntransp = ntransp.sort(["from_zone", "to_zone"])
#ntransp['from_by_zone'] = by_zone
#ntransp['to_by_zone'] = by_zone

#print("after sorting")
#print(ntransp.head())

eta = ntransp.pivot(index="from_by_zone", columns="to_by_zone", values="flow")
#eta = ntransp.select(
#        lambda s : (s == "from_by_zone")
#                or (s == "to_by_zone")
#                or (s == "from_zone")
#                or (s == "to_zone")
#                or (s == "flow"),
#        axis=1)
eta = eta.fillna(value=0)

for tbz in (np.arange(260) + 1) :
  try :
    eta.loc[:, tbz]
  except KeyError :
    eta.loc[:, tbz] = 0

for fbz in (np.arange(260) + 1) :
  try :
    eta.loc[fbz, :]
  except KeyError :
    eta.loc[fbz, :] = 0

eta = eta.sort()

for fbz in np.arange(260) + 1 :
  for tbz in np.arange(260) + 1 :
    if eta.loc[fbz, tbz] != eta.loc[tbz, fbz] :
      if eta.loc[fbz, tbz] == 0 :
        eta.loc[fbz, tbz] = eta.loc[tbz, fbz]
      elif eta.loc[tbz, fbz] == 0 :
        eta.loc[tbz, fbz] = eta.loc[fbz, tbz]
      else :
        print(fbz, tbz, eta.loc[fbz, tbz], eta.loc[tbz, fbz])
        raise ValueError("The matrix can't be made diagonal")

eta = eta.sort(axis=1)

# compute the mean rate of immigration per habitant across cities
eta_nrm = eta.copy()
for tbz in np.arange(260) + 1 :
  eta_nrm.loc[:, tbz] = eta.loc[:, tbz] / Nca[tbz - 1]

eta_tot = eta_nrm.sum(axis=0)
eta_mean = eta_tot.mean()
eta = eta / eta_mean
# WARNING ! This makes for very high rates

cities = cities.sort("zone")
cities["by_zone"] = by_zone
cities_subset = cities.select(
                  lambda s : (s == 'by_zone') 
                             or (s == 'zone') 
                             #or (s == 'city')
                             or (s == 'population'),
                  axis=1)

df = pd.merge(left=df, 
              right=cities_subset, 
              how='outer',
              left_on='city_newind',
              right_on='by_zone')

df['inc_nmz'] = df['inc'] / df['population'] * 100000
df['log(inc)'] = np.log(df['inc_nmz'] + 1)
df.to_csv("/home/queue/Documents/2015stage/data/C_g_10_vals.csv")
eta.to_csv("/home/queue/Documents/2015stage/data/eta.csv")
