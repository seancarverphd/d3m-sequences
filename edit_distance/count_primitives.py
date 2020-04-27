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

unique_problems = set(problems.problem) 

n = 0
n_primitives = []
u_problems = list(unique_problems)
for u_problem in u_problems:
    problems_one_type = problems[problems['problem'] == u_problem]
    seq_list = [] 
    for sequence in problems_one_type['sequence']:
        seq_list.append(sequence)
    seq = '-'.join(seq_list)
    n_primitives.append(len(set(seq.split(sep='-'))))

print(pd.DataFrame({'problem': u_problems, 'number_primitives': n_primitives}))
print("Max number of primitives:", max(n_primitives))
