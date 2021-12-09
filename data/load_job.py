import json
from . import translate

def load_job_json(jpn_job_name):
    kor_job_name = translate.get_job_name('jpn', 'kor', jpn_job_name)
    with open('data/job/'+kor_job_name+'.json', 'rt', encoding='UTF-8') as f:
        json_data = json.load(f)
    return json_data
