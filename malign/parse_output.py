import matplotlib
import numpy as np
import pandas as pd
import pickle
import sys
sys.path.insert(1, '/home/sean/Code/d3m-sequences/show_graph')
import show_graph

with open("single_problem_data.pickle", "rb") as f:
    sp = pickle.load(f)

with open("outma0.hex", "r") as f:
    lines = f.readlines()

k = 0
with open("outma0.txt", "w") as f:
    n_non = 0
    i = 0
    for line in lines:
        if line[0:8] != 'pipeline':
            print(line[0:8], 'NOT A PIPELINE:', line)
            n_non += 1
            continue
        pipeline_num = int(line[9:13])
        pipeline_col = show_graph.performer_colors[sp[k]['performers'][i]]
        assert pipeline_num == sp[k]['pipeline_num'][i]
        f.write('@color{' +
                str(matplotlib.colors.to_rgb(pipeline_col)[0]) + ' ' +
                str(matplotlib.colors.to_rgb(pipeline_col)[1]) + ' ' +
                str(matplotlib.colors.to_rgb(pipeline_col)[2]) + '}' +
                '{:<10}'.format(sp[k]['performers'][i]) + line)
        i += 1

