import os
import pickle

import make_one_ma_input
import parse_output
import list_primitives

prob = 21

with open("single_problem_data.pickle", "rb") as f:
    sp = pickle.load(f)

make_one_ma_input.run_one_ma(prob)
parse_output.parsein(prob)
theheader = sp[prob]['type']
os.system('enscript --landscape -b '+theheader+' -v -e@ outma'+str(prob)+'.txt -o - | ps2pdf - outma'+str(prob)+'.pdf')
list_primitives.list_all_primitives()
os.system("enscript -B -v -e@ primitive_list.txt -o - | ps2pdf - primitive_list.pdf")

