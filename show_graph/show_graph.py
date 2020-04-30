import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import pickle
import random

import networkx as nx

with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)

performer_colors = {'cmu':'red', 'isi':'orange', 'mit':'yellow', 'nyu':'green', 'nyu_2':'blue', 'sri':'purple', 'tamu':'grey', 'ucb':'brown', 'uncharted':'pink'}

def compute_one(i, seed=None, performer2watch=None):
    G = nx.Graph()
    maxd = 0
    node_labels = single_problems[i]['pipeline_num']
    n_nodes = len(node_labels)
    G.add_nodes_from(node_labels)
    cols = [performer_colors[k] for k in single_problems[i]['performers']]
    for a in range(n_nodes-1):  # looping over all unique pairs of nodes
        for b in range(a+1, n_nodes):  # looping over all unique pairs of nodes
            dist = single_problems[i]['distances'][a,b]
            if single_problems[i]['performers'][a] == performer2watch and single_problems[i]['performers'][b] == performer2watch:  # selects performer2watch for pairwise comparisons
                print(dist, single_problems[i]['pipeline_2'][a], single_problems[i]['pipeline_2'][b])  # prints distance, and both sequences
            if maxd < dist:  # to figure out maximum distance for problem
                maxd = dist
            similarity = 1000. if dist == 0 else 1./dist 
            G.add_edge(node_labels[a], node_labels[b], weight=similarity)
    if performer2watch:  # performer2watch used as an analysis flag, see above
        print("Maximum distance:", maxd)
    pos = nx.spring_layout(G, seed=seed)
    return G, pos, cols

def show_Gpos(G, pos, cols):
    nx.draw(G, pos, node_color=cols, with_labels=True, edgelist=[])
    plt.show()

def show_one(i):
    G, pos, cols = compute_one(i)
    show_Gpos(G, pos, cols)

