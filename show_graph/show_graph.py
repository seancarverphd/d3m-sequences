import matplotlib
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import pickle
import random
import seaborn as sns
import sys

import networkx as nx

sys.path.insert(1, '/home/sean/Code/d3m-sequences/edit_distance/')
import edit_norm

with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)

performer_colors = {'cmu':'red', 'isi':'darkorange', 'mit':'gold', 'nyu':'green', 'nyu_2':'blue', 'sri':'purple', 'tamu':'darkslategrey', 'ucb':'brown', 'uncharted':'deeppink'}


def dist2sim(dist):
    return 1000. if dist == 0 else 1./dist 

def compute_one(i, seed=None, performer2watch=None):
    G = nx.Graph()
    maxd = 0
    node_labels = single_problems[i]['pipeline_num']
    n_nodes = len(node_labels)
    n_edges_left = n_nodes*(n_nodes-1)/2
    G.add_nodes_from(node_labels)
    cols = [performer_colors[k] for k in single_problems[i]['performers']]
    for a in range(n_nodes-1):  # looping over all unique pairs of nodes
        for b in range(a+1, n_nodes):  # looping over all unique pairs of nodes
            dist = single_problems[i]['distances'][a,b]
            if single_problems[i]['performers'][a] == performer2watch and single_problems[i]['performers'][b] == performer2watch:  # selects performer2watch for pairwise comparisons
                print(dist, single_problems[i]['pipeline_2'][a], single_problems[i]['pipeline_2'][b])  # prints distance, and both sequences
            if maxd < dist:  # to figure out maximum distance for problem
                maxd = dist
            similarity = dist2sim(dist)
            G.add_edge(node_labels[a], node_labels[b], weight=similarity)
            n_edges_left -= 1
    assert n_edges_left == 0
    if performer2watch:  # performer2watch used as an analysis flag, see above
        print("Maximum distance:", maxd)
    pos = nx.spring_layout(G, seed=seed, iterations=1000)
    return G, pos, cols

def show_Gpos(G, pos, cols):
    nx.draw(G, pos, node_color=cols, with_labels=True, edgelist=[])
    plt.show()

def show_one(i, seed=None):
    G, pos, cols = compute_one(i, seed)
    show_Gpos(G, pos, cols)

def print_one(i, seed=None, fname='fig'):
    matplotlib.use('Agg')  # plt.ioff()
    show_one(i, seed)
    plt.savefig(fname+'.eps', format='eps')
    plt.close('all')

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

def cor_metrics(i, x_metric, y_metric):
    df = edit_norm.multimeasure(prob=i)
    if df is None:
        print("df is None")
        return None
    elif len(df) < 3:
        print('length of dataframe =', len(df))
        return None
    r = df[x_metric].corr(df[y_metric])
    if np.isnan(r) and df[x_metric].std()*df[y_metric].std() == 0:
        print('Scatter plot vertical or horizontal')
        return None
    else:
        return r

def show_scatter(i,x_metric, y_metric):
    df = edit_norm.multimeasure(prob=i)
    sns.scatterplot(data=df, x=x_metric, y=y_metric)
    r = cor_metrics(i, x_metric, y_metric)
    try:
        plt.title(edit_norm.problem_name(prob=i) + ': r='+ f'{r:.2f}')
    except:
        plt.title(edit_norm.problem_name(prob=i))
        print("Cannot show r (NaN?)")
    if x_metric == 'max_score':
        plt.xlabel('MAX. ' + edit_norm.adjusted_metric(prob=i))
    label_point(df[x_metric], df[y_metric], df.index.to_series(), plt.gca())

def collect_cors(x_metric, y_metric):
    names = []
    cors = []
    for i in range(len(single_problems)):
        print(i)
        names.append(edit_norm.problem_name(i))
        cors.append(cor_metrics(i, x_metric, y_metric))
    return pd.DataFrame({'name': names, 'num': range(len(single_problems)), 'r': cors})

def plot_cors(df, x_metric, y_metric):
    sns.distplot(df.r, kde=False, bins=20)
    plt.title("Each case is a performer/problem/dataset and at least 3 pipelines")
    plt.xlabel("Correlation between "+x_metric+" and "+y_metric)
    plt.ylabel("Count of cases in bin")


