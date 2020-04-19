import json
import os
import pickle

import config

institution_dirs = os.listdir(config.data_home)
n_submissions = 0
n_pipelines = 0
n_primitives = 0
pipeline_list = []
primitive_set = set()
n_load_failures = 0
for institution_dir in institution_dirs:
    submissions = os.listdir(config.data_home + '/' + institution_dir)
    n_submissions += len(submissions)
    for submission in submissions:
        try:
            with open(config.sets_home + submission + '/' + submission + '_problem/problemDoc.json') as f:
                d = json.load(f)  # parse problem metadata json
        except:
            print(submission + ' fails to load')
            n_load_failures += 1
            continue  # next submission
        keywords = d['about']['taskKeywords']
        often_just_one = os.listdir(config.data_home + institution_dir + '/' + submission)
        assert len(often_just_one) == 1
        pipelines = os.listdir(config.data_home + institution_dir + '/' + submission + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked')
        for pipeline in pipelines:
            if pipeline[-4:] == 'rank':  # should have both .rank file and .json file and nothing else
                continue  # next file in pipeline directory
            else:
                assert pipeline[-4:] == 'json'
                with open(config.data_home + institution_dir + '/' + submission + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked/' + pipeline) as f:
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
print(n_load_failures, "Failures to Load")
print(len(institution_dirs), "Institutional Directories")
print(n_submissions, "Submissions") 
print(n_pipelines, "Pipelines")
print(n_primitives, "Primitives")
print(len(primitive_set), "Unique Primitives")
assert len(institution_dirs) == 10
assert n_submissions == 955
assert n_pipelines == 9672  # without 27 load failures would be 9910
assert n_primitives == 109227  # without 27 load failures would be 111682
assert len(primitive_set) == 231 # without 27 load failues would be 232 
with open(config.parse_save, 'wb') as f:
    pickle.dump(pipeline_list, f)

