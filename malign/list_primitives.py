import pickle

def list_all_primitives():

    with open("pipelines.pickle", "rb") as f:
        pipelines = pickle.load(f)

    with open("translators.pickle", "rb") as f:
        ta = pickle.load(f)
        tb = pickle.load(f)

    plist = []
    for p in pipelines: 
        for j in range(len(p['primitives'])): 
            plist.append((p['primitives'][j], p['names'][j]))

    print(len(set(plist)))
    pset = set(plist)
    primitives = sorted([tb[p[0]]+': '+p[1] for p in pset])

    with open("primitive_list.txt", "w") as f:
        for p in primitives:
            f.write(p+"\n")
