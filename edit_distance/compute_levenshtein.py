import numpy as np
import pandas as pd
import pickle
from Levenshtein import distance
import sys

sys.path.insert(1, '/home/sean/Code/d3m-sequences/file_crawler/')
from list_metrics import isCost

def translator(inp, trans):
    return [trans[x] for x in inp]

def transform(inp,outp):
    all_characters_list = [chr(k) for k in range(0x21, 0x7f)]
    all_characters_string = ''.join(all_characters_list)
    hex_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    hex2 = [h1+h0 for h1 in hex_digits for h0 in hex_digits]
    ma_alphabets = [h for h in hex2 if h not in {'00', '3e', '3d', '3c', '2d', '20', '0d', '0a'} ]

    with open(inp, "rb") as f:  # inp = "problems.pickle" by default
        problems = pickle.load(f)

    n_primitives = []
    problems_data = []
    unique_problems = set(problems['problem'])
    u_problems = list(unique_problems)
    u_problems.sort()
    prob_num = 0

    for u_problem in u_problems:
        problems_one_type = problems[problems['problem'] == u_problem]
        # The numbers '2' and '1', below, denote the number of bytes per alphabet in sequences.
        list2_pipelines = [sequence2 for sequence2 in problems_one_type['sequence']]  # list of pipeline sequences, 2 character, for just one problme
        concat2_pipelines = '-'.join(list2_pipelines)  # joining all pipelines as a string, repeating primitives
        # The notation '_primitives_used_for_problem' indicates all unique primitives across all pipelines for just one problem
        set2_primitives_used_for_problem = set(concat2_pipelines.split(sep='-'))  # contains just the unique primitives
        list2_primitives_used_for_problem = list(set2_primitives_used_for_problem)
        string2_primitives_used_for_problem = '-'.join(list2_primitives_used_for_problem)
        n_primitives_used_for_problem = len(list2_primitives_used_for_problem)
        trans21 = {primitive2 : primitive1
                for (primitive2, primitive1) in zip(list2_primitives_used_for_problem, all_characters_list[:n_primitives_used_for_problem])}
        trans12 = {primitive1 : primitive2
                for (primitive2, primitive1) in zip(list2_primitives_used_for_problem, all_characters_list[:n_primitives_used_for_problem])}
        trans2h = {primitive2 : primitiveh
                for (primitive2, primitiveh) in zip(list2_primitives_used_for_problem, ma_alphabets[:n_primitives_used_for_problem])}
        transh2 = {primitiveh : primitive2
                for (primitive2, primitiveh) in zip(list2_primitives_used_for_problem, ma_alphabets[:n_primitives_used_for_problem])}
        # u_problem is problem type
        list1_pipelines = [''.join(translator(pipeline2.split('-'), trans21)) for pipeline2 in list2_pipelines]
        listh_pipelines = [' '.join(translator(pipeline2.split('-'), trans2h)) for pipeline2 in list2_pipelines]
        list_ids_pipelines = [ident for ident in problems_one_type['pipeline']]
        list_nums_pipelines = list(problems_one_type['num'])
        list_performers_pipelines = [performer for performer in problems_one_type['performer']]
        list_adjusted_score_pipelines = [score for score in problems_one_type['adjusted_score']]
        list_metric_pipelines = ['-'+m if isCost[m] else m for m in problems_one_type['metric']]
        lev_dist = np.zeros([len(list1_pipelines), len(list1_pipelines)])
        node0pair = []
        node1pair = []
        performer0pair = []
        performer1pair = []
        distancepair = []
        if prob_num == 0: print(u_problem, list_nums_pipelines)
        prob_num += 1
        for i in range(len(list1_pipelines)):
            for j in range(len(list1_pipelines)):
                lev_dist[i,j] = distance(list1_pipelines[i], list1_pipelines[j]) 
                if j > i:
                    node0pair.append(list_nums_pipelines[i])
                    node1pair.append(list_nums_pipelines[j])
                    performer0pair.append(list_performers_pipelines[i])
                    performer1pair.append(list_performers_pipelines[j])
                    distancepair.append(lev_dist[i,j])
        pairs_df = pd.DataFrame({'node0': node0pair, 'node1': node1pair, 
            'performers0': performer0pair, 'performers1': performer1pair,
            'distance': distancepair})
        problem_dictionary = {'type': u_problem,
                'keywords': problems_one_type.iloc[0,2],
                'all_primitives_used': string2_primitives_used_for_problem,
                'translator2h': trans2h,
                'translatorh2': transh2,
                'translator21': trans21,
                'translator12': trans12,
                'pipeline_h': listh_pipelines,
                'pipeline_1': list1_pipelines,
                'pipeline_2': list2_pipelines,
                'pipeline_num': list_nums_pipelines,
                'pipeline_ids': list_ids_pipelines,
                'performers': list_performers_pipelines,
                'adjusted_scores': list_adjusted_score_pipelines,
                'adjusted_metric': list_metric_pipelines,
                'distances': lev_dist,
                'pairs': pairs_df}
        problems_data.append(problem_dictionary)
        n_primitives.append(n_primitives_used_for_problem)

    print(pd.DataFrame({'problem': u_problems, 'number_primitives': n_primitives}))
    print("Max number of primitives:", max(n_primitives))
    print(len(all_characters_string), "Characters in Alphabet Set:", all_characters_string)

    with open(outp, "wb") as f:  # outp = "single_problem_data.pickle" by default
        pickle.dump(problems_data, f)

transform("problems.pickle", "single_problem_data.pickle")

