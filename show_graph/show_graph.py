import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import pickle

import networkx as nx

with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)

performer_colors = {'cmu':'red', 'isi':'orange', 'mit':'yellow', 'nyu':'green', 'nyu_2':'blue', 'sri':'purple', 'tamu':'black', 'ucb':'brown', 'uncharted':'pink'}

def compute_one(i):
    G = nx.Graph()
    node_labels = single_problems[i]['pipeline_num']
    n_nodes = len(node_labels)
    G.add_nodes_from(node_labels)
    for a in range(n_nodes-1):
        for b in range(a+1, n_nodes):
            dist = single_problems[i]['distances'][a,b]
            similarity = 1000. if dist == 0 else 1./dist 
            G.add_edge(node_labels[a], node_labels[b], weight=similarity)
            # G.add_edge(a, b, weight=dist)
    pos = nx.spring_layout(G)
    return G, pos

def show_Gpos(G, pos):
    # nx.draw_networkx_labels(G, pos)
    nx.draw(G, pos, with_labels=True, edgelist=[])
    plt.show()

def show_one(i):
    G, pos = compute_one(i)
    show_Gpos(G, pos)

def test32(c=1., d=2.):
    H = nx.Graph()
    H.add_node(0)
    H.add_node(1)
    H.add_node(2)
    H.add_node(4)
    H.add_node(5)
    H.add_edge(0, 1, weight = c/1.)
    H.add_edge(0, 2, weight = c/1.)
    H.add_edge(1, 2, weight = c/1.)
    H.add_edge(4, 5, weight = c/1.)
    H.add_edge(0, 4, weight = c/d)
    H.add_edge(0, 5, weight = c/d)
    H.add_edge(1, 4, weight = c/d)
    H.add_edge(1, 5, weight = c/d)
    H.add_edge(2, 4, weight = c/d)
    H.add_edge(2, 5, weight = c/d)
    pos = nx.spring_layout(H)
    return H, pos
