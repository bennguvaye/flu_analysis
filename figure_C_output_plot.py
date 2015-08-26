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
import matplotlib.gridspec as gs
from matplotlib.dates import DateFormatter
import seaborn as sb

def to_map_heatmap(*args, **kwargs) :
  print(args)
  #print(kwargs)
  data = kwargs.pop('data')
  to_plot = data.pivot(index=args[0], columns=args[1], values=args[2])
  print(to_plot.head())
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
eta_file = "/home/queue/Documents/2015stage/data/eta.csv"
eta = pd.read_csv(eta_file)

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
#subs_mex = df[df['city_newind'] == 1]
subs_mex = df[df['by_zone'] == 1]
del df
subs_rep_st = subs_g[(subs_g['rep']==3) & (subs_g['strain']==1)]
subs_rep_st = subs_rep_st.select(
         lambda s : ((s == 'by_zone') 
                     #or (s == 'city_newind') 
                     or (s == 't') 
                     or (s == 'zone') 
                     or (s == 'log(inc)')), 
         axis=1)

#subs_rep_st = subs_rep_st.sort('zone')
#subs_rep_st["by_zone"] = np.arange(subs_rep_st.shape[0])
print(subs_rep_st.head())
vmin = subs_rep_st['log(inc)'].min()
vmax = subs_rep_st['log(inc)'].max()

from_south = (eta['from_by_zone'] <= 20)
from_tropi = (eta['from_by_zone'] > 20) & (eta['from_by_zone'] <= 80)
from_north = (eta['from_by_zone'] > 80)

to_south = (eta['from_by_zone'] <= 20)
to_tropi = (eta['from_by_zone'] > 20) & (eta['from_by_zone'] <= 80)
to_north = (eta['from_by_zone'] > 80)

# The nine eta submatrices
eta_ss = eta.iloc[1:21, 1:21]
eta_se = eta.iloc[1:21, 21:81]
eta_sn = eta.iloc[1:21, 81:]
eta_es = eta.iloc[21:81, 1:21]  
eta_ee = eta.iloc[21:81, 21:81] 
eta_en = eta.iloc[21:81, 81:]   
eta_ns = eta.iloc[81:, 1:21]
eta_ne = eta.iloc[81:, 21:81]
eta_nn = eta.iloc[81:, 81:]

subs_rep_st_south = subs_rep_st[subs_rep_st['zone']==-1]
subs_rep_st_eq = subs_rep_st[subs_rep_st['zone']==0]
subs_rep_st_north = subs_rep_st[subs_rep_st['zone']==1]

#srs_pivot = subs_rep_st.pivot(index='city_newind', columns='t', values='log(inc)')
#srs_pivot = subs_rep_st.pivot(index='city_newind', columns='t')
srs_pivot = subs_rep_st.pivot(index='by_zone', columns='t', values='log(inc)')
srsn_pivot = subs_rep_st_north.pivot(index='by_zone', columns='t', values='log(inc)')
srse_pivot = subs_rep_st_eq.pivot(index='by_zone', columns='t', values='log(inc)')
srss_pivot = subs_rep_st_south.pivot(index='by_zone', columns='t', values='log(inc)')

f0 = plt.figure()
a00 = f0.add_subplot(111)
sb.heatmap(srs_pivot, ax=a00, xticklabels=30, yticklabels=10)

grid = gs.GridSpec(13, 34)

f1 = plt.figure()
f1.set_label("log(incidence + 1) for all cities")

# FIXME make eta symmetric ?
# FIXME add in vmin, vmax...
# FIXME put that stuff in a for loop
# FIXME make a clusterplot somehow ? (with the split plot ?)

cbar_eta_ax = plt.subplot(grid[:, 13])
a1nn = plt.subplot(grid[0:9, 0:9])
sb.heatmap(eta_nn,
           ax=a1nn,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1nn.set_xlabel("")
a1nn.set_ylabel("north")

a1ne = plt.subplot(grid[0:9, 9:12])
sb.heatmap(eta_ne,
           ax=a1ne,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ne.set_xlabel("")
a1ne.set_ylabel("")

a1ns = plt.subplot(grid[0:9, 12])
sb.heatmap(eta_ns,
           ax=a1ns,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ns.set_xlabel("")
a1ns.set_ylabel("")

a1en = plt.subplot(grid[9:12, 0:9])
sb.heatmap(eta_en,
           ax=a1en,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1en.set_xlabel("")
a1en.set_ylabel("tropics")

a1ee = plt.subplot(grid[9:12, 9:12])
sb.heatmap(eta_ee,
           ax=a1ee,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ee.set_xlabel("")
a1ee.set_ylabel("")

a1es = plt.subplot(grid[9:12, 12])
sb.heatmap(eta_es,
           ax=a1es,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1es.set_xlabel("")
a1es.set_ylabel("")

a1sn = plt.subplot(grid[12, 0:9])
sb.heatmap(eta_sn,
           ax=a1sn,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1sn.set_xlabel("")
a1sn.set_ylabel("south")

a1se = plt.subplot(grid[12, 9:12])
sb.heatmap(eta_se,
           ax=a1se,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1se.set_xlabel("")
a1se.set_ylabel("")

a1ss = plt.subplot(grid[12, 12])
sb.heatmap(eta_ss,
           ax=a1ss,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ss.set_xlabel("")
a1ss.set_ylabel("")

a_cbar = plt.subplot(grid[:, 33])
#a10 = f1.add_subplot(311)
a10 = plt.subplot(grid[0:9, 14:33])
sb.heatmap(srsn_pivot, 
           ax=a10, 
           xticklabels=False, 
           yticklabels=False, 
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a10.set_ylabel("")
#a10.set_ylabel("north")
#a11 = f1.add_subplot(312)
a11 = plt.subplot(grid[9:12, 14:33])
sb.heatmap(srse_pivot, 
           ax=a11, 
           xticklabels=False, 
           yticklabels=False,
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a11.set_ylabel("")
#a11.set_ylabel("tropics")
#a12 = f1.add_subplot(313)
a12 = plt.subplot(grid[12, 14:33])
sb.heatmap(srss_pivot, 
           ax=a12, 
           xticklabels=104, 
           yticklabels=False,
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a12.set_ylabel("")
#a12.set_ylabel("south") 
#formatter = DateFormatter('%Y')
#a12.xaxis.set_major_formatter(formatter)
a12.xaxis_date()
f1.autofmt_xdate()

#g1 = sb.FacetGrid(subs_rep_st, row='zone')
#g1.map_dataframe(to_map_heatmap,
#                 'city_newind', 
#                 't', 
#                 'log(inc)',
#                 xticklabels=30,
#                 yticklabels=10,
#                 #vmin=subs_rep_st['inc_nmz'].min(),
#                 #vmax=subs_rep_st['inc_nmz'].max(),
#                 cmap=color_map,
#                 cbar=True)

#g2 = sb.FacetGrid(subs_mex, hue='rep', row='g_ind', col='strain')
#g2.map(plt.plot, 't', 'inc_nmz')

#subs_g_mex = subs_g[subs_g['city_newind'] == 1]
#g3 = sb.FacetGrid(subs_g_mex, row='rep', col="strain")
#g3.map(plt.plot, 't', 'inc_nmz')

plt.show()
