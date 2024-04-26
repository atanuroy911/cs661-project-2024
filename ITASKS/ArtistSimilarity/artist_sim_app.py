import os
import json
import dash
import numpy as np
import networkx as nx
from dash import dcc, html
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

# load the artist mapping containing the artist corresponding to the matrix
artist_map = None

with open("./artist_map.json", 'r') as file:
    artist_map = json.load(file)
print("Added artist-index mappings for the adjacency matrix")

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
                          color=color,
                          shape="spline"),
                hoverinfo='none',
                mode='lines')

# calculates thickness of edge depending on weight
def weight_to_width_scale(x):
    return (x**20)

import matplotlib.cm as cm

def map_to_color(value, cmap='viridis'):
    """
    Convert a number to an RGBA color value based on a colormap.

    Parameters:
        value (float): Number between 0 and 1.
        cmap_name (str): Name of the colormap. Default is 'viridis'.

    Returns:
        str: RGBA color value in the format 'rgba( , , , )'.
    """
    cmap = plt.get_cmap(cmap)
    color = cmap(1-value)
    rgba_string = "rgba({}, {}, {}, {})".format(int(color[0] * 255),int(color[1] * 255),int(color[2] * 255),0.4)
    return rgba_string

def get_n_distinct_colors(n, cmap="rainbow"):
    cmap = plt.get_cmap(cmap)
    colors = [cmap(i) for i in np.linspace(0, 1, n)]
    colors = ["rgba({}, {}, {}, {})".format(int(color[0]*255),int(color[1]*255),int(color[2]*255),1) for color in colors]
    return colors

def node_strength(node, G):
    strength = 0
    neighbors = set(G.neighbors(node))
    for neighbor in neighbors:
        strength += G.edges[node, neighbor]["weight"]
    
    return strength

trace_dict = dict()

for k in [1,3,5,7,9]:
    # load the cosine similarity based adjacency matrix
    artist_similarity = np.load(f'./artist_similarity_{k}.npy')
    print(f"Loaded artist similarity for k={k}")
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
    
    pos = nx.spring_layout(G, weight=0.1)

    # add artist positions to the graph object
    for key, val in pos.items():
        G.nodes[key]['pos'] = pos[key]
    
    # trace objects to be provided to plotly figure
    data_trace_list = []
    # scaling (down) factor of weight
    edging_scaling = np.max(artist_similarity[:20][:20])

    # adds edges' traces to the data_trace_list
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edging = make_edge(
            x = tuple([x0, x1, None]),
            y = tuple([y0, y1, None]),
            width = 3*weight_to_width_scale(G.edges[edge]['weight']/edging_scaling),
            color = map_to_color(G.edges[edge]['weight']/edging_scaling, cmap="viridis")
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
        mode='markers+text',
        hoverinfo='none',
        textposition="top center",
        textfont=dict(
            size=16
        ),
        marker=dict(
            showscale=False,
            colorscale='Rainbow',
            reversescale=True,
            color=get_n_distinct_colors(20, cmap="rainbow"),
            opacity=0.5,
            size=15,
            line_width=1))
    node_trace.text = artist_map["artist_list"][:20]
    
    node_power = [node_strength(node, G) for node in artist_map["artist_list"][:20]]
    node_power = [node_pow/max(node_power) for node_pow in node_power]
    node_trace.marker.size = [25*(node_pow**3) for node_pow in node_power]

    data_trace_list.append(node_trace)
    trace_dict[k] = data_trace_list
    print(f"Added data trace for k = {k}")


# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.Label('Choose value of k:'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'k = 1', 'value': 1},
            {'label': 'k = 3', 'value': 3},
            {'label': 'k = 5', 'value': 5},
            {'label': 'k = 7', 'value': 7},
            {'label': 'k = 9', 'value': 9}
        ],
        value=1  # Default value
    ),
    dcc.Graph(id='graph')
])

# Define callback to update the graph based on dropdown value
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_value):
    # Create trace based on selected value
    trace = trace_dict[selected_value]
    # Create layout
    layout = go.Layout(
                    title='Artist Similarity Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=100),
                    annotations=[ dict(
                        text = f"Number of nearest neighbours considered = {selected_value}",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    
    # Return figure
    return {'data': trace, 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)