import pickle
import numpy as np
import random

with open("input.pickle", "rb") as f:
    _ = pickle.load(f)
    _ = pickle.load(f)
    c = pickle.load(f)

# N = 50  # for debugging
# n = 10  # for debugging
N = len(c)  # for running
n = 10000  # for running
random.seed(1)

list_of_pairs = []
for i in range(N):
    for j in range(i-1):
        list_of_pairs.append((j,i))

sampled_pairs = random.sample(list_of_pairs, n)

with open("sampled_pairs.pickle","wb") as f:
    pickle.dump(sampled_pairs, f)
