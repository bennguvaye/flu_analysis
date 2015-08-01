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

df = pd.read_csv("/home/queue/Documents/2015stage/data/C_g_10_vals.csv")

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

subs_g = df[df['g_ind'] == 0]
subs_mex = df[df['city_newind'] == 1]
del df
subs_rep_st = subs_g[(subs_g['rep']==1) & (subs_g['strain']==1)]
subs_rep_st = subs_rep_st.select(
         lambda s : ((s == 'zone') 
                     or (s == 'city_newind') 
                     or (s == 't') 
                     or (s == 'inc_nmz')), 
         axis=1)

subs_rep_st = subs_rep_st.pivot('city_newind', 't', 'inc_nmz')

g1 = sb.FacetGrid(subset, row='zone')
g1.map_dataframe(to_map_heatmap,
                 't', 
                 'city_newind', 
                 'inc_nmz',
                 xticklabels=False,
                 yticklabels=False,
                 vmin=subset['inc_nmz'].min(),
                 vmax=subset['inc_nmz'].max(),
                 cmap=color_map)

g2 = sb.FacetGrid(subs_mex, hue='rep', row='g_ind', col='strain')
g2.map(plt.plot, 't', 'inc')

subs_g_mex = subs_g[subs_g['city_newind'] == 1]
g3 = sb.FacetGrid(subs_g_mex, row='rep', col="strain")
g3.map(plt.plot, 't', 'inc_nmz')

plt.show()
