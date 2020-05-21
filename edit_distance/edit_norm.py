import pickle
import numpy as np

with open("single_problem_data.pickle", "rb") as f:
    sp = pickle.load(f)

def lpnorm(prob, p, normalize=False):
    df = sp[prob]['pairs']
    if p == np.Inf and normalize:
        print(df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (max(dfr.distance)/len(dfr.distance))))
    elif normalize:
        print(df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance**p))**(1/p)/len(dfr.distance)))
    elif p == np.Inf:
        print(df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (max(dfr.distance))))
    else:
        print(df[df.performers0 == df.performers1].groupby('performers0').apply(lambda dfr: (sum(dfr.distance**p))**(1/p)))



