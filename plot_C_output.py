#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

"""
This script plots interesting data about the output from the full simulation
C program.

"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

def to_map_heatmap(*args, **kwargs) :
  data = kwargs.pop('data')
  to_plot = data.pivot(*args)
  return sb.heatmap(to_plot, **kwargs)

color_map = sb.cubehelix_palette(start=0.1, 
                                 rot=0.8, 
                                 gamma=1.2, 
                                 light=0.85,
                                 dark=0.15,
                                 as_cmap=True)
color_map.set_under(color='white')
color_map.set_over(color='black')

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

# we start by plotting the aggregated (on cities) data for both strains
c0 = 238 
n0 = "New-York"
c1 = 257
n1 = "Washington"
c2 = 138 
n2 = "Mexico"
c3 = 1  
n3 = "Buenos Aires"
c4 = 164 
n4 = "Singapour"
c5 = 10 
n5 = "Sydney"
c6 = 68
n6 = "Havane"
c7 = 4
n7 = "Cairns"

cl = [c0, c1, c2, c3, c4, c5, c6, c7]
nl = [n0, n1, n2, n3, n4, n5, n6, n7]

c = np.arange(260)
# TODO arranger les villes dans un ordre bien selon la location géographique
# on voit pas des tonnes les deux phases...
# aussi faire les deux souches indépendamment pour voir si ya quelque chose à voir

#f2 = plt.figure()
#a2 = f2.add_subplot(111)
#p3 = a2.pcolormesh(t, c, np.transpose(strain_0 + strain_1), cmap=color_map)
#plt.colorbar(p3)

subset = df[(df['g_ind']==0) & (df['rep']==1) & (df['strain']==1)]

subset = subset.select(
         lambda s : ((s == 'zone') 
                     or (s == 'city_newind') 
                     or (s == 't') 
                     or (s == 'inc')), 
         axis=1)

# subset = subset.pivot('city_newind', 't', 'inc')

#g1 = sb.FacetGrid(subset, row='zone')
#g1.map_dataframe(to_map_heatmap,
#                 't', 
#                 'city_newind', 
#                 'inc',
#                 xticklabels=False,
#                 yticklabels=False,
#                 vmin=subset['inc'].min(),
#                 vmax=subset['inc'].max(),
#                 cmap=color_map)

#df_mexico = df[df['city_newind'] == 1]
#g2 = sb.FacetGrid(df_mexico, hue='rep', row='g_ind', col='strain')
#g2.map(plt.plot, 't', 'inc')

df_mex_0 = df_mexico[df_mexico['g_ind'] == 0]
g3 = sb.FacetGrid(df_mexico, col='rep', col_wrap=2)
g3.map(plt.plot, 't', 'inc')

plt.show()
