import pickle
from sgt import Sgt

# with open("input.pickle", "rb") as f:
with open("sgt.pickle", "rb") as f:
    corpus = pickle.load(f)
#    alphabets = pickle.load(f)
#    pipeline_list = pickle.load(f)
#    code2id = pickle.load(f)
#    id2code = pickle.load(f)

s_g_t = Sgt(kappa=5, lengthsensitive=True)

s = s_g_t.fit_transform(corpus)

with open("sgt_output.pickle", "wb") as f:
    pickle.dump(s, f)

