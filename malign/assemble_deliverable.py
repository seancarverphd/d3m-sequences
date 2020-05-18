import os
import pickle

with open("single_problem_data.pickle", "rb") as f:
    sp = pickle.load(f)

st = sorted(range(len(sp)), key=lambda k: sp[k]['type'])                                                                                                                                           
print([sp[k]['type'] for k in st])

file_list = ["outma"+str(k)+".pdf" for k in st]

writeup = "../writeup/pipelines_in_problems.pdf"

files = ' '.join(file_list)

os.system("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=deliverable.pdf " + writeup + " " + files + " primitive_list.pdf") 


