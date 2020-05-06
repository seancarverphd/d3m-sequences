import pandas as pd
import pickle

with open("single_problem_data.pickle","rb") as f:
    sp = pickle.load(f)

with open("ma0.hex","w+") as f:
    for i, pipeline in enumerate(sp[0]['pipeline_h']):
        f.write(">pipeline_"+str(sp[0]['pipeline_num'][i])+"\n")
        f.write(pipeline+"\n")

