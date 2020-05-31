import numpy as np
import pandas as pd
import pickle

def lpnorm(prob=0, p=1, normalize=False, inp="single_problem_data.pickle"):
    with open(inp, "rb") as f:
        sp = pickle.load(f)
    df = sp[prob]['pairs']
    if p == 0 and normalize:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance!=0)/len(dfr.distance))).sort_values(ascending=False)
    elif p == np.Inf and normalize:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (max(dfr.distance)/len(dfr.distance))).sort_values(ascending=False)
    elif normalize and p!=0:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance**p))**(1/p)/len(dfr.distance)).sort_values(ascending=False)
    elif p == np.Inf:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (max(dfr.distance))).sort_values(ascending=False)
    elif p == 0:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance!=0))).sort_values(ascending=False) 
    else:
        return df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance**p))**(1/p)).sort_values(ascending=False)

def max_score(prob=0):
    with open("single_problem_data.pickle", "rb") as f:
        sp = pickle.load(f)
    df = pd.DataFrame({"performer": sp[prob]['performers'], "adjusted_score": sp[prob]['adjusted_scores']})
    return df.groupby('performer').max().sort_values('adjusted_score', ascending=False)

def multimeasure(prob=0):
    common_index = set()
    l1 = pd.DataFrame(lpnorm(prob=prob, p=1))
    l1.columns = ['l1']
    l2 = pd.DataFrame(lpnorm(prob=prob, p=2))
    l2.columns = ['l2']
    linf = pd.DataFrame(lpnorm(prob=prob, p=np.inf))
    linf.columns = ['linf']
    maxs = pd.DataFrame(max_score(prob=prob))
    maxs.columns = ['max_score']
    multi = pd.DataFrame(l1).join(pd.DataFrame(l2),how='inner').join(pd.DataFrame(linf),how='inner').join(pd.DataFrame(maxs),how='inner')
    return multi

def problem_name(prob=0):
    with open("single_problem_data.pickle", "rb") as f:
        sp = pickle.load(f)
    return sp[prob]['type']
