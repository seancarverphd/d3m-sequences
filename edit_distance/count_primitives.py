import numpy as np
import pandas as pd
import pickle

with open("pipelines.pickle", "rb") as f:
    pipelines = pickle.load(f)
with open("problems.pickle", "rb") as f:
    problems = pickle.load(f)
with open("translators.pickle", "rb") as f:
    c2i = pickle.load(f)
    i2c = pickle.load(f)

all_characters_list = [chr(k) for k in range(0x21, 0x7f)]
all_characters_string = ''.join(all_characters_list)

n_primitives = []

unique_problems = set(problems['problem']) 
u_problems = list(unique_problems)
for u_problem in u_problems:
    problems_one_type = problems[problems['problem'] == u_problem]
    pipeline_list = [] 
    for pipeline_sequence in problems_one_type['sequence']:
        pipeline_list.append(pipeline_sequence)
    concat_pipelines = '-'.join(pipeline_list)  # joining all pipelines, repeating primitives
    set_primitives2_for_problem = set(concat_pipelines.split(sep='-'))  # contains just the unique primitives
    list_primitives2_for_problem = list(set_primitives2_for_problem)
    string_primitives2_for_problem = '-'.join(list_primitives2_for_problem)
    n_primitives.append(len(list_primitives2_for_problem))

print(pd.DataFrame({'problem': u_problems, 'number_primitives': n_primitives}))
print("Max number of primitives:", max(n_primitives))
print(len(all_characters_string), "Characters in Alphabet Set:", all_characters_string)

