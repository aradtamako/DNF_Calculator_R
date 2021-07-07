import json


def load_job_json(job_name):
    with open('data/job/'+job_name+'.json', 'rt', encoding='UTF-8') as f:
        json_data = json.load(f)
    return json_data
