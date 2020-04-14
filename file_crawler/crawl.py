import json
import os

import config

institution_dirs = os.listdir(config.data_home)
n_submissions = 0
n_pipelines = 0
n_primitives = 0
for institution_dir in institution_dirs:
    submissions = os.listdir(config.data_home + '/' + institution_dir)
    n_submissions += len(submissions)
    for submission in submissions:
        often_just_one = os.listdir(config.data_home + '/' + institution_dir + '/' + submission)
        assert len(often_just_one) == 1
        pipelines = os.listdir(config.data_home + '/' + institution_dir + '/' + submission + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked')
        for pipeline in pipelines:
            if pipeline[-4:] == 'rank':
                continue
            else:
                assert pipeline[-4:] == 'json'
                with open(config.data_home + '/' + institution_dir + '/' + submission + '/' + often_just_one[0] + '/EVALUATION/pipelines_ranked/' + pipeline) as f:
                    d = json.load(f)
                list_of_step_ids = []
                for step in d['steps']:
                    list_of_step_ids.append(step['primitive']['id'])
                new_pipeline = {'pipeline' : d['id'], 'primitives' : list_of_step_ids}
                n_pipelines += 1
                n_primitives += len(d['steps'])
print(len(institution_dirs), "Institutional Directories")
print(n_submissions, "Submissions") 
print(n_pipelines, "Pipelines")
print(n_primitives, "Primitives")
