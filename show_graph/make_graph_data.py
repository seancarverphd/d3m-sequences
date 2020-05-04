import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

import networkx as nx

import show_graph 

with open("pipelines.pickle", "rb") as f:
    pipelines = pickle.load(f)
with open("problems.pickle", "rb") as f:
    problems = pickle.load(f)
with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)
with open("translators.pickle", "rb") as f:
    translators = pickle.load(f)

nodes = []
edges = []
for i, problem in enumerate(single_problems):
    G, pG, cG = show_graph.compute_one(i, seed=i)
    nodes.append(pd.DataFrame({'pipeline_number': problem['pipeline_num'],
                              'sequence': problem['pipeline_2'],
                              'id': problem['pipeline_ids'],
                              'performer': problem['performers'],
                              'xpos': [pG[key][0] for key in pG],
                              'ypos': [pG[key][1] for key in pG],
                              'color': cG}))
    node0s = []
    node1s = []
    dists = []
    similarities = []
    node_labels = problem['pipeline_num']
    n_nodes = len(node_labels)
    for a in range(n_nodes-1):  # looping over all unique pairs of nodes
        for b in range(a+1, n_nodes):  # looping over all unique pairs of nodes
            node0s.append(node_labels[a])
            node1s.append(node_labels[b])
            dist = problem['distances'][a,b]
            dists.append(dist)
            similarities.append(show_graph.dist2sim(dist))
    edges.append(pd.DataFrame({'node0': node0s, 'node1': node1s, 'distance': dists, 'similarity': similarities}))

with open("made_graph_data.pickle","wb") as f:
    pickle.dump(nodes, f)
    pickle.dump(edges, f)
