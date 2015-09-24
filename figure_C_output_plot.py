#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtc
import matplotlib.gridspec as gs
#from matplotlib.dates import DateFormatter, YearLocator
import seaborn as sb

"""
This script plots interesting data about the output from the full simulation
C program, reading data from C_new_vals.csv.

"""

# script argument : 10 reps (0-9) to choose from
rep = int(sys.argv[1])

def to_map_heatmap(*args, **kwargs) :
  """Heatmap plotting function for FacetGrid."""
  print(args)
  #print(kwargs)
  data = kwargs.pop('data')
  to_plot = data.pivot(index=args[0], columns=args[1], values=args[2])
  print(to_plot.head())
  return sb.heatmap(to_plot, **kwargs)

def sb_plot(*args, **kwargs) :
  """Simple plotting function for FacetGrid."""
  data = kwargs.pop('data')
  ind = args[0]
  val = args[1]
  return data.plot(ind, val, **kwargs)

# Create seaborn colormaps
color_map_i = sb.cubehelix_palette(start=0.1, 
                                 rot=0.9, 
                                 gamma=1.2, 
                                 light=0.95,
                                 dark=0.15,
                                 as_cmap=True)
color_map_i.set_under(color='white')
color_map_i.set_over(color='black')

color_map_eta = sb.cubehelix_palette(start=0.1, 
                                 rot=1.5, 
                                 gamma=1.2, 
                                 light=0.95,
                                 dark=0.1,
                                 as_cmap=True)
color_map_eta.set_under(color='white')
color_map_eta.set_over(color='black')

# Read the data
df = pd.read_csv("/home/queue/Documents/2015stage/data/C_new_vals.csv")
eta_file = "/home/queue/Documents/2015stage/data/eta.csv"
eta = pd.read_csv(eta_file)

subs_rep = df[(df['rep']==rep)]
#del df
subs_rep = subs_rep.select(
         lambda s : ((s == 'by_zone') 
                     #or (s == 'city_newind')
                     or (s == 'strain')
                     or (s == 't') 
                     or (s == 'zone') 
                     or (s == 'log(inc)')), 
         axis=1)

print(subs_rep.head())
vmin = subs_rep['log(inc)'].min()
vmax = subs_rep['log(inc)'].max()

# air traffic as log10
eta = np.log(eta + 1) / np.log(10)
# The nine eta submatrices (sn : south-north)
eta_ss = eta.iloc[1:21, 1:21]
eta_se = eta.iloc[1:21, 21:81]
eta_sn = eta.iloc[1:21, 81:]
eta_es = eta.iloc[21:81, 1:21]  
eta_ee = eta.iloc[21:81, 21:81] 
eta_en = eta.iloc[21:81, 81:]   
eta_ns = eta.iloc[81:, 1:21]
eta_ne = eta.iloc[81:, 21:81]
eta_nn = eta.iloc[81:, 81:]

# Three zones
subs_rep_south = subs_rep[subs_rep['zone']==-1]
subs_rep_eq = subs_rep[subs_rep['zone']==0]
subs_rep_north = subs_rep[subs_rep['zone']==1]

srs_pivot = subs_rep.pivot_table(index='by_zone', 
                                 columns='t', 
                                 values='log(inc)',
                                 aggfunc=np.sum)
srsn_pivot = subs_rep_north.pivot_table(index='by_zone', 
                                        columns='t', 
                                        values='log(inc)',
                                        aggfunc=np.sum)
srse_pivot = subs_rep_eq.pivot_table(index='by_zone', 
                                     columns='t', 
                                     values='log(inc)',
                                     aggfunc=np.sum)
srss_pivot = subs_rep_south.pivot_table(index='by_zone', 
                                        columns='t', 
                                        values='log(inc)',
                                        aggfunc=np.sum)

# Layout
grid = gs.GridSpec(13, 34)

f1 = plt.figure()
f1.set_label("log(incidence + 1) for all cities")

# FIXME put that stuff in a for loop # yeah well
# FIXME make a clusterplot somehow ? (with the split plot ?) 
  # try it but impossible with the split plot ?

############################# Plot the airflow data ###########################
# left colorbar
cbar_eta_ax = plt.subplot(grid[:, 13])
a1nn = plt.subplot(grid[0:9, 0:9])
a1nn.set_title("(a)", weight="demi", size="large", loc="left")
sb.heatmap(eta_nn,
           ax=a1nn,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1nn.set_xlabel("")
a1nn.set_ylabel("north")

a1ne = plt.subplot(grid[0:9, 9:12])
sb.heatmap(eta_ne,
           ax=a1ne,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ne.set_xlabel("")
a1ne.set_ylabel("")

a1ns = plt.subplot(grid[0:9, 12])
sb.heatmap(eta_ns,
           ax=a1ns,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ns.set_xlabel("")
a1ns.set_ylabel("")

a1en = plt.subplot(grid[9:12, 0:9])
sb.heatmap(eta_en,
           ax=a1en,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1en.set_xlabel("")
a1en.set_ylabel("tropics")

a1ee = plt.subplot(grid[9:12, 9:12])
sb.heatmap(eta_ee,
           ax=a1ee,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ee.set_xlabel("")
a1ee.set_ylabel("")

a1es = plt.subplot(grid[9:12, 12])
sb.heatmap(eta_es,
           ax=a1es,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1es.set_xlabel("")
a1es.set_ylabel("")

a1sn = plt.subplot(grid[12, 0:9])
sb.heatmap(eta_sn,
           ax=a1sn,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1sn.set_xlabel("")
a1sn.set_ylabel("south")

a1se = plt.subplot(grid[12, 9:12])
sb.heatmap(eta_se,
           ax=a1se,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1se.set_xlabel("")
a1se.set_ylabel("")

a1ss = plt.subplot(grid[12, 12])
sb.heatmap(eta_ss,
           ax=a1ss,
           cmap=color_map_eta,
           cbar_ax=cbar_eta_ax,
           xticklabels=False,
           yticklabels=False)
a1ss.set_xlabel("")
a1ss.set_ylabel("")
cbar_eta_ax.yaxis.set_ticklabels([])

######################## Plot the full model output data ######################

a_cbar = plt.subplot(grid[:, 33])
a10 = plt.subplot(grid[0:9, 14:33])
a10.set_title("(b)", weight="demi", size="large", loc="left")
sb.heatmap(srsn_pivot, 
           ax=a10, 
           xticklabels=False, 
           yticklabels=False, 
           cmap=color_map_i,
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a10.set_ylabel("")
a10.set_yticklabels([])
a11 = plt.subplot(grid[9:12, 14:33])
sb.heatmap(srse_pivot, 
           ax=a11, 
           xticklabels=False, 
           yticklabels=False,
           cmap=color_map_i,
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a11.set_ylabel("")
a11.set_yticklabels([])
a12 = plt.subplot(grid[12, 14:33])
sb.heatmap(srss_pivot, 
           ax=a12, 
           # reduce the number of ticks
           xticklabels=260,
           yticklabels=False,
           cmap=color_map_i,
           cbar_ax=a_cbar,
           vmin=vmin,
           vmax=vmax)
a12.set_ylabel("")
# plots the time in years
def fmter(n, pos) :
  return "{:.0f}".format(10 + n / 26)
formatter = mtc.FuncFormatter(fmter)
a12.xaxis.set_major_formatter(formatter)

######################### Plotting some reps of the data ######################

# Plots time series for the chosen cities
subs_some = df[
   ((df['city_newind'] == 238)
    | (df['city_newind'] == 32)
    | (df['city_newind'] == 23)
    | (df['city_newind'] == 260)
    | (df['city_newind'] == 1)
    | (df['city_newind'] == 146))
  & (df['rep'] == rep)]

subs_some = subs_some.sort("by_zone")
subs_some = subs_some.sort("t")

g2 = sb.FacetGrid(subs_some, hue='strain', row='city',
                  row_order=["NEW YORK", "BEIJING", 
                             "HO CHI MINH CITY", "RIO DE JANEIRO",
                             "BUENOS AIRES", "WELLINGTON"],
                  size=1.5, aspect=5, sharey=False)
g2 = g2.map_dataframe(sb_plot, 't', 'inc_nmz') #marker=".", linestyle=' ')
g2.set_ylabels("")
g2.fig.suptitle("(c)", weight="demi", size="large", x=0.)

#plt.show()

f1.savefig("/home/queue/Documents/2015stage/plots/full_model_new_r" + str(rep) + ".png", 
           dpi=300)

g2.savefig("/home/queue/Documents/2015stage/plots/full_model_new_some_r" + str(rep) + ".png", 
           dpi=300)

