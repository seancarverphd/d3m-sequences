import json
import os
import pickle
import random

import config

random.seed(0)

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

performers = os.listdir(config.data_home)
for performer in performers:
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
        unique_submissions = unique_submissions.union({submission})
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
                with open(config.data_home + performer + '/' + problem + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked/' + pipeline) as f:
                    d = json.load(f)  # parse pipeline json
                list_of_step_ids = []
                list_of_names = []
                # Create ids and names of primitives
                for step in d['steps']:
                    list_of_step_ids.append(step['primitive']['id'])
                for step in d['steps']:
                    list_of_names.append(step['primitive']['name'])
                # Create dictionary for pipeline
                pipeline_list.append({'pipeline' : d['id'], 'keywords' : keywords, 'primitives' : list_of_step_ids, 'names' : list_of_names})
                # Update list of unique IDs
                primitive_set = primitive_set.union(set(list_of_step_ids))
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

# Print counts for sanity check
print(n_load_failures, "Failures to Load")
print(len(performers), "Performers")
print(len(problem_set), "Problems")
print(n_submissions, "Submissions") 
print(len(unique_submissions), "Unique Submissions")
print(n_pipelines, "Pipelines")
print(n_primitives, "Primitives")
print(len(primitive_set), "Unique Primitives")

# Assert that counts haven't changed so can investigate if they have
assert len(performers) == 10
assert n_submissions == 955
assert n_pipelines == 9672  # without 27 load failures would be 9910
assert n_primitives == 109227  # without 27 load failures would be 111682
assert len(primitive_set) == 231 # without 27 load failues would be 232 

# Dump data
with open(config.parse_save, 'wb') as f:
    pickle.dump([pipeline['sequence_list'] for pipeline in pipeline_list], f)  # dump corpus
    pickle.dump([id2code[primitive] for primitive in primitive_set], f)  # dump alphabets
    pickle.dump(pipeline_list, f)  # dump list of pipeline dictionaries
    pickle.dump(code2id, f)  # dump code to id translator
    pickle.dump(id2code, f)  # dump reverse translator

