import os
import pandas as pd
import pickle

with open("single_problem_data.pickle","rb") as f:
    sp = pickle.load(f)

def make_one_ma(prob):
    with open("ma"+str(prob)+".hex","w+") as f:
        for i, pipeline in enumerate(sp[prob]['pipeline_h']):
            f.write(">pipeline_"+str(sp[prob]['pipeline_num'][i])+"\n")
            f.write(pipeline+"\n")

def run_one_ma(prob):
    make_one_ma(prob)
    os.system("hex2maffttext ma"+str(prob)+".hex > ma"+str(prob)+".ASCII")
    os.system("mafft --text --clustalout ma"+str(prob)+".ASCII > outma"+str(prob)+".ASCII")
    os.system("maffttext2hex outma"+str(prob)+".ASCII > outma"+str(prob)+".hex")

