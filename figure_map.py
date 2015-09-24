
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
# plot graphs
import networkx as nx
# plot maps
from mpl_toolkits import basemap as bm

root_path = "/home/queue/Documents/2015stage/data/"
cities = pd.read_csv(root_path + "260villes.csv")
transport = pd.read_csv(root_path + "260transport2009.dat", sep=";", decimal=",")

G = nx.Graph()
carte = bm.Basemap()

# Build the graph
max_flow = transport['flow'].max()
for _, line in cities.iterrows() :
  G.add_node(line['newid'], pos=carte(line['longitude'], line['latitude']))

for _, line in transport.iterrows() :
  G.add_edge(line['from'], line['to'], alpha=line['flow'] / max_flow)

pos = nx.get_node_attributes(G, 'pos')
alpha = nx.get_edge_attributes(G, 'alpha')

# Draw the graph
for _, line in transport.iterrows() :
  nx.draw_networkx_edges(G, 
                         pos=pos,
                         edgelist=[[line['from'], line['to']]],
                         arrows=False, 
                         with_labels=False, 
                         width=4 * line['flow'] / (1000 + line['flow']),
                         alpha=0.9 * line['flow'] / (3000 + line['flow']))
               
# Draw the map  
carte.drawcoastlines()
plt.suptitle("(c)", size="x-large", x=0.1, y=0.8)
plt.savefig("/home/queue/Documents/2015stage/plots/eta_map.png", dpi=300) 
