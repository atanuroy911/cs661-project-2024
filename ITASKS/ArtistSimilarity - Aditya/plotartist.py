# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import networkx as nx


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('./'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


import os
import json
import seaborn
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# load the cosine similarity based adjacency matrix
artist_similarity = np.load('artist_similarity.npy')
print("loaded artist similarity")


# load the artist mapping containing the artist corresponding to the matrix
artist_map = None

with open("artist_map.json", 'r') as file:
    artist_map = json.load(file)
print("Added artist-index mappings for the adjacency matrix")

# Builds an empty graph
G = nx.Graph()

# Graph nodes are artist names
G.add_nodes_from(artist_map["artist_list"][:20])

# add weighted edges
for i in range(20):
    for j in range(i+1, 20):
        G.add_edge(
            artist_map["artist_list"][i],
            artist_map["artist_list"][j],
            weight= artist_similarity[i][j]
        )
    artist = artist_map["artist_list"][i]
    
print(list(G.edges)[0])

print(G.edges['Rabindra Nath Tagore','Raihan Sharif'])

pos = nx.random_layout(G) #<-- change this to change graph layout


count = 0
# pos contains 2d euclidean distances
for key, val in pos.items():
    print(f"{key} -> {val}")
    count += 1
    if count == 5:
        break
    
    
for key, val in pos.items():
    G.nodes[key]['pos'] = pos[key]
#     print(f"Added positions for artist {key}.")


G.nodes['Rabindra Nath Tagore']


# creates an edge for plotly go object
def make_edge(x, y, width, color):
    """
    Args:
        x: a tuple of the x from and to, in the form: tuple([x0, x1, None])
        y: a tuple of the y from and to, in the form: tuple([y0, y1, None])
        width: The width of the line

    Returns:
        a Scatter plot which represents a line between the two points given. 
    """
    return  go.Scatter(
                x=x,
                y=y,
                line=dict(width=width,
                          color=color),
                hoverinfo='none',
                mode='lines')
    
    
# trace objects to be provided to plotly figure
data_trace_list = []


# edge
G.edges[('Rabindra Nath Tagore','Raihan Sharif')]


# scaling (down) factor of weight
edging_scaling = np.max(artist_similarity[:20][:20])
print(edging_scaling)


# calculates thickness of edge depending on weight
def weight_to_width_scale(x):
    return ( -0.5 + (1 / ( 1 + np.exp(-x)) ) )


import matplotlib.colors as mcolors
# calculates edge color depending on weight
def map_to_color(value):
    # Normalize value to range [0, 1]
    value = max(0, min(1, value))

    # Choose colormap
    cmap = plt.get_cmap('YlGnBu')

    # Map normalized value to RGBA color
    rgba_color = cmap(value)

    # Convert RGBA to HEX color code
    hex_color = mcolors.rgb2hex(rgba_color)

    return hex_color

# Example usage
value = 0.75
color = map_to_color(value)
print("Color for value", value, ":", color)


# adds edges' traces to the data_trace_list
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edging = make_edge(
        x = tuple([x0, x1, None]),
        y = tuple([y0, y1, None]),
        width = 7*weight_to_width_scale(G.edges[edge]['weight']/edging_scaling),
        color = map_to_color(G.edges[edge]['weight']/edging_scaling)
    )
    data_trace_list.append(edging)
    
    
# finally add nodes' traces
node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
#         color=[],
        size=10,
        line_width=1))


node_trace.text = artist_map["artist_list"][:20]


data_trace_list.append(node_trace)


# build the figure
fig = go.Figure(data=data_trace_list,
             layout=go.Layout(
                title='Artist Similarity Graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()
fig.write_html('ArtistSimilarity.html')