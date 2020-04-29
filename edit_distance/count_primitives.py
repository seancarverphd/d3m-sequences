import numpy as np
import pandas as pd
import pickle
# from Levenshtein import distance as levenshtein_distance

def translator(inp, trans):
    return [trans[x] for x in inp]

with open("pipelines.pickle", "rb") as f:
    pipelines = pickle.load(f)
with open("problems.pickle", "rb") as f:
    problems = pickle.load(f)
with open("translators.pickle", "rb") as f:
    c2i = pickle.load(f)
    i2c = pickle.load(f)

all_characters_list = [chr(k) for k in range(0x21, 0x7f)]
all_characters_string = ''.join(all_characters_list)

trans_pipeline_id_num = {pipelines[i]['pipeline'] : i for i in range(len(pipelines))}  # Converts id to num

n_primitives = []
problems_data = []

unique_problems = set(problems['problem']) 
u_problems = list(unique_problems)
for u_problem in u_problems:
    problems_one_type = problems[problems['problem'] == u_problem]
    list2_pipelines = [sequence2 for sequence2 in problems_one_type['sequence']]
    concat2_pipelines = '-'.join(list2_pipelines)  # joining all pipelines as a string, repeating primitives
    set2_primitives_used_for_problem = set(concat2_pipelines.split(sep='-'))  # contains just the unique primitives
    list2_primitives_used_for_problem = list(set2_primitives_used_for_problem)
    string2_primitives_used_for_problem = '-'.join(list2_primitives_used_for_problem)
    n_primitives_used_for_problem = len(list2_primitives_used_for_problem)
    trans21 = {primitive2 : primitive1
            for (primitive2, primitive1) in zip(list2_primitives_used_for_problem, all_characters_list[:n_primitives_used_for_problem])}
    trans12 = {primitive1 : primitive2
            for (primitive2, primitive1) in zip(list2_primitives_used_for_problem, all_characters_list[:n_primitives_used_for_problem])}
    # u_problem is problem type
    list1_pipelines = [''.join(translator(pipeline2.split('-'), trans21)) for pipeline2 in list2_pipelines]
    list_ids_pipelines = [ident for ident in problems_one_type['pipeline']]
    list_nums_pipelines = [trans_pipeline_id_num[ident] for ident in problems_one_type['pipeline']]
    list_performers_pipelines = [performer for performer in problems_one_type['performer']]
    problem_dictionary = {'type': u_problem,
            'all_primitives_used': string2_primitives_used_for_problem,
            'translator21': trans21,
            'translator12': trans12,
            'pipeline_1': list1_pipelines,
            'pipeline_2': list2_pipelines,
            'pipeline_num': list_nums_pipelines,
            'pipeline_ids': list_ids_pipelines,
            'performers': list_performers_pipelines}
    problems_data.append(problem_dictionary)
    n_primitives.append(n_primitives_used_for_problem)

print(pd.DataFrame({'problem': u_problems, 'number_primitives': n_primitives}))
print("Max number of primitives:", max(n_primitives))
print(len(all_characters_string), "Characters in Alphabet Set:", all_characters_string)

with open("single_problem_data.pickle","wb") as f:
    pickle.dump(problems_data, f)

