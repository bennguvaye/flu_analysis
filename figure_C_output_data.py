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

Nc_file = "/home/queue/Documents/2015stage/code/C/data/N.dat"
g_file = "/home/queue/Documents/2015stage/data/C_g_10_pars.csv"
eta_file = "/home/queue/Documents/2015stage/data/eta.csv"

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
  strain_1['t'] = np.linspace(0, n * dt * prntime / 365, n)
  strain_2['t'] = np.linspace(0, n * dt * prntime / 365, n)
  
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

out_l = [ get_g_data(g_ind) for g_ind in range(5) ] # FIXME change to 10 eventually
df = pd.concat(out_l)


cities_subset = cities.select(
                  lambda s : (s == 'newid') 
                             or (s == 'zone') 
                             or (s == 'city')
                             or (s == 'population'),
                  axis=1)

df = pd.merge(left=df, 
              right=cities_subset, 
              how='outer',
              left_on='city_newind',
              right_on='newid')

df['inc_nmz'] = df['inc'] / df['population'] * 100000

df.to_csv("/home/queue/Documents/2015stage/data/C_g_10_vals.csv")
