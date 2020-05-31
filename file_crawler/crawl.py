import json
import numpy as np
import os
import pandas as pd
import pickle
import random

import config
import list_metrics

random.seed(0)

problem_col = []
performer_col = []
pipeline_col = []
sequence_col = []
metric_col = []
value_col = []
adjusted_score_col = []
normalized_col = []
randomSeed_col = []
fewer_performers = 0
n_submissions = 0
n_pipelines = 0
n_primitives = 0
pipeline_list = []
unique_submissions = set()
primitive_set = set()
problem_set = set()
n_load_failures = 0
problems_that_failed_to_load_metadata = set()

debug = 0
delta_unique_submissions = []
cannotopenscores = 0
cannotloadscores = 0

performers = os.listdir(config.data_home)
for performer in performers:
    if performer == 'tamu_2':  # Eliminate this performer with only 1 problem and 1 pipeline as per S. Stanley's instructions
        fewer_performers += 1
        continue
    submissions = os.listdir(config.data_home + '/' + performer)
    n_submissions += len(submissions)  # A "submission" is a "(performer, problem)"
    for problem in submissions:
        n_failed_problems = len(problems_that_failed_to_load_metadata)
        try:
            with open(config.sets_home + problem + '/' + problem + '_problem/problemDoc.json') as f:
                d = json.load(f)  # parse problem metadata json
        except:
            problems_that_failed_to_load_metadata = problems_that_failed_to_load_metadata.union({problem})  # add problem to list of failures
            if len(problems_that_failed_to_load_metadata) > n_failed_problems:  # indicates new failure with differently named problem
                print('PROBLEM METADATA FAILS TO LOAD:', problem)
            n_load_failures += 1
            continue  # next problem
        submission = performer + '/' + problem
        n_unique_submissions_old = len(unique_submissions)
        unique_submissions = unique_submissions.union({submission})
        delta_unique_submissions.append(len(unique_submissions) - n_unique_submissions_old)
        problem_set = problem_set.union({problem})  # only increases if problem represents a new problem
        keywords = d['about']['taskKeywords']
        often_just_one = os.listdir(config.data_home + performer + '/' + problem)
        assert len(often_just_one) == 1
        pipelines = os.listdir(config.data_home + performer + '/' + problem + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked')
        for pipeline in pipelines:
            if pipeline[-4:] == 'rank':  # should have both .rank file and .json file and nothing else
                continue  # next file in pipeline directory
            else:
                assert pipeline[-4:] == 'json'
                score_filename = config.data_home + performer + '/' + problem + '/' + often_just_one[0] + '/EVALUATION/score/' + pipeline[:-4] + "score.csv"
                try:  # load scores 
                    f = open(score_filename)
                except:
                    if cannotopenscores==0:
                        print('Cannot open file.  Does not exist?  See count below.  First failure: ' + score_filename)
                    cannotopenscores += 1
                    continue
                try:
                    score_df = pd.read_csv(f)
                except:
                    if cannotloadscores==0:
                        print('Cannot load csv file.  Empty?  See count below.  First failure: ' + score_filename)
                    cannotloadscores += 1
                    continue
                f.close()
                # Parse Scores
                assert(len(score_df)==1)
                metric = score_df['metric'][0]
                value = score_df['value'][0]
                adjusted_score = -value if list_metrics.isCost[metric] else value
                normalized = score_df['normalized'][0]
                randomSeed = score_df['randomSeed'][0]
                # Load pipeline json without scores
                with open(config.data_home + performer + '/' + problem + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked/' + pipeline) as f:
                    d = json.load(f)  # parse pipeline json
                # Parse pipeline json
                list_of_step_ids = []
                list_of_names = []
                # Create ids and names of primitives
                for step in d['steps']:
                    list_of_step_ids.append(step['primitive']['id'])
                for step in d['steps']:
                    list_of_names.append(step['primitive']['name'])
                # Create dictionary for pipeline
                pipeline_list.append({'pipeline': d['id'], 'keywords': keywords, 'primitives': list_of_step_ids, 'names': list_of_names,
                    'metric': metric, 'value': value, 'adjusted_score': adjusted_score,
                    'normalized': normalized, 'randomSeed': randomSeed, 'score_filename': score_filename,
                    'problem': problem, 'performer': performer})
                # Update list of unique IDs
                primitive_set = primitive_set.union(set(list_of_step_ids))
                # Update df_problem
                problem_col.append(problem)
                performer_col.append(performer)
                pipeline_col.append(d['id'])
                metric_col.append(metric)
                value_col.append(value)
                adjusted_score_col.append(adjusted_score)
                normalized_col.append(normalized)
                randomSeed_col.append(randomSeed)
                # too slow: df_problem = pd.concat([df_problem, pd.DataFrame([problem, performer, d['id']], index=(['problem', 'performer', 'pipeline']))])
                # Update counts
                n_pipelines += 1
                n_primitives += len(d['steps'])
# Create list of letters
caps_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
caps_list = [char for char in caps_string]

# Create list of all possible 2-letter codes
conceivable_codes = []
for letter0 in caps_list:
    for letter1 in caps_list:
        conceivable_codes.append(letter0+letter1)  # construct list of two letter codes
codes = random.sample(conceivable_codes, len(primitive_set))  # prune list and randomize order

# Create translation dictionaries
code2id = {}
id2code = {}
for code, primitive_id in zip(codes, primitive_set):
    code2id[code] = primitive_id
    id2code[primitive_id] = code

# Create sequences for each pipeline in dictionary
for pipeline in pipeline_list:  # each "pipeline" is a dictionary
    sequence_list = []
    for primitive in pipeline['primitives']:  # each primitive is a shah1 hash (or similar ID)
        sequence_list.append(id2code[primitive])  # appending a 2-letter code (eg ['AB', 'CD'])
    pipeline['sequence_list'] = sequence_list
    sequence_string = sequence_list[0]  # create a string concatenating codes (eg 'AB-CD') in sequence_list; '-' separating; easier way?
    for i in range(len(sequence_list) - 1):
        sequence_string += '-' + sequence_list[i+1]
    pipeline['sequence_string'] = sequence_string
    sequence_col.append(pipeline['sequence_string'])

# Print counts for sanity check
print(n_load_failures, "Failures to Load Problem Metadata Counting Performer Repeats")
print(len(performers) - fewer_performers, "Performers Not Counting tamu_2")
print(len(problem_set), "Problems Not Counting Failures")
print(n_submissions, "Submissions Including Those That Fail To Load Problem Metadata") 
print(len(unique_submissions), "Unique Submissions Not Including Failures")
print("All", len(delta_unique_submissions), "Unique:", all([x == 1 for x in delta_unique_submissions])) 
print(n_pipelines, "Pipelines")
print(n_primitives, "Primitives")
print(len(primitive_set), "Unique Primitives")
print(1, "Maximum number of scores")
print(cannotloadscores, "Score failed to load.  File exists but empty?")
print(cannotopenscores, "Score failed to open.  File does not exist?")

df_problem = pd.DataFrame({'problem': problem_col, 'performer': performer_col, 'pipeline': pipeline_col, 'sequence': sequence_col, 'num': range(len(problem_col)),
                'metric': metric_col, 'value': value_col, 'adjusted_score': adjusted_score_col, 'normalized': normalized_col, 'randomSeed': randomSeed})

# Assert that counts haven't changed so can investigate if they have
assert len(performers) == 10
assert n_submissions == 954  # one less without tamu_2
assert n_pipelines == 9022  # 9671 but some w/no scores; without 1 for tamu_2 and 27 load failures would be 9910
assert n_primitives == 101216  # 109201 not excluding w/o scores; without 26 primitives from tamu_2 and the primitives in 27 load failures would be 111682
assert len(primitive_set) == 216  # 222 w/no scores, without 9 primitives unique to tamu_2's pipeline plus unique primitives from the 27 load failues would be 232
assert cannotloadscores == 639
assert cannotopenscores == 10

# Dump data
with open(config.sgt_data, 'wb') as f:
    pickle.dump([pipeline['sequence_list'] for pipeline in pipeline_list], f)  # dump corpus
    pickle.dump([id2code[primitive] for primitive in primitive_set], f)  # dump alphabets

with open(config.pipeline_data, 'wb') as f:
    pickle.dump(pipeline_list, f)  # dump list of pipeline dictionaries

with open(config.translators, 'wb') as f:
    pickle.dump(code2id, f)  # dump code to id translator
    pickle.dump(id2code, f)  # dump reverse translator

with open(config.problem_data, 'wb') as f:
    pickle.dump(df_problem, f) # dump the problem DataFrame
