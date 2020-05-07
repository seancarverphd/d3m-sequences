import copy
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

prob = 0
d = sp[prob]['translatorh2']
d['--'] = '--'
with open("outma0.txt", "w") as f:
    n_nonpipeline = 0
    i_pipeline_in_problem = 0
    for line in lines:
        if line[0:8] != 'pipeline':
            n_nonpipeline += 1
            continue
        pipeline_num = int(line[9:13])
        rest_of_line = line[13:]
        line_pieces = rest_of_line.split(' ')
        line_pieces_copy = copy.deepcopy(line_pieces)
        i = len(line_pieces_copy)
        for piece in line_pieces_copy[::-1]:
            i -= 1  # step from end to front of list to avoid changing index when popping
            if len(piece) != 2:
                line_pieces.pop(i)
        pipeline2 = '-'.join([d[piece] for piece in line_pieces])
        print(pipeline2)
        pipeline_col = show_graph.performer_colors[sp[prob]['performers'][i_pipeline_in_problem]]
        assert pipeline_num == sp[prob]['pipeline_num'][i_pipeline_in_problem]
        f.write('@color{' +
                str(matplotlib.colors.to_rgb(pipeline_col)[0]) + ' ' +
                str(matplotlib.colors.to_rgb(pipeline_col)[1]) + ' ' +
                str(matplotlib.colors.to_rgb(pipeline_col)[2]) + '}' +
                '{:<10}'.format(sp[prob]['performers'][i_pipeline_in_problem]) + line[:14] + pipeline2 + '\n')
        i_pipeline_in_problem += 1  # shouldn't increment if nonpipeline

