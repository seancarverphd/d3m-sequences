import numpy as np
import pandas as pd
import pickle

with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)

def lpnorm(prob=0, p=1, normalize=False, inp=None):  # None loads: single_problem_data.pickle
    if inp is not None:
        with open(inp, "rb") as f:
            sp = pickle.load(f)
    else:
        sp = single_problems
    df = sp[prob]['pairs']
    repeated_performers = df[df.performers0 == df.performers1]
    if len(repeated_performers) == 0:
        print("lp_norm: No performer had more than one pipeline.")
        return None
    grouped_performers = repeated_performers.groupby('performers0')
    if p == 0 and normalize:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance!=0)/len(dfr.distance))).sort_values(ascending=False)
    elif p == np.Inf and normalize:
        return grouped_performers.apply(lambda dfr: (max(dfr.distance)/len(dfr.distance))).sort_values(ascending=False)
    elif normalize and p!=0:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance**p))**(1/p)/len(dfr.distance)).sort_values(ascending=False)
    elif p == np.Inf:
        return grouped_performers.apply(lambda dfr: (max(dfr.distance))).sort_values(ascending=False)
    elif p == 0:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance!=0))).sort_values(ascending=False) 
    else:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance**p))**(1/p)).sort_values(ascending=False)

def count_pipelines(prob=0, inp="single_problem_data.pickle"):
    pass 

def max_score(prob=0):
    with open("single_problem_data.pickle", "rb") as f:
        sp = pickle.load(f)
    df = pd.DataFrame({"performer": sp[prob]['performers'], "adjusted_score": sp[prob]['adjusted_scores']})
    return df.groupby('performer').max().sort_values('adjusted_score', ascending=False)

def multimeasure(prob=0):
    common_index = set()
    l1 = pd.DataFrame(lpnorm(prob=prob, p=1))
    if len(l1) == 0:
        return None
    l1.columns = ['l1']
    l2 = pd.DataFrame(lpnorm(prob=prob, p=2))
    if len(l2) == 0:
        return None
    l2.columns = ['l2']
    linf = pd.DataFrame(lpnorm(prob=prob, p=np.inf))
    if len(linf) == 0:
        return None
    linf.columns = ['linf']
    maxs = pd.DataFrame(max_score(prob=prob))
    if len(maxs) == 0:
        return None
    maxs.columns = ['max_score']
    multi = pd.DataFrame(l1).join(pd.DataFrame(l2),how='inner').join(pd.DataFrame(linf),how='inner').join(pd.DataFrame(maxs),how='inner')
    return multi

def problem_name(prob=0):
    with open("single_problem_data.pickle", "rb") as f:
        sp = pickle.load(f)
    return sp[prob]['type']

def adjusted_metric(prob=0):
    with open("single_problem_data.pickle", "rb") as f:
        sp = pickle.load(f)
    return sp[prob]['adjusted_metric'][0]

