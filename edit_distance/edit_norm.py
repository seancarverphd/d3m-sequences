import pickle
import numpy as np

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

# def max_score(prob=0, 

