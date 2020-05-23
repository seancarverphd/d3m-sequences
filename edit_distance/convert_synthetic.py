import pandas as pd
import pickle

import compute_levenshtein

def convert(fname='p2'):
    df = pd.read_csv(fname+'.csv')
    with open(fname+'.pkl','wb') as f:
        pickle.dump(df, f)
    compute_levenshtein.transform(fname+'.pkl', fname+'.pickle')

convert(fname='p2')
