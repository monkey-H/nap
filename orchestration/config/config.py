import yaml
import os

def read(file_path):
    if not os.path.isfile(file_path):
        return '-'

    f = open(file_path)
    config = yaml.safe_load(f)

    srv_dicts = []

    for item in config:
    	srv_dict = {}
    	srv_dict['name'] = item
    	for key in config[item]:
    		srv_dict[key] = config[item][key]
    	srv_dicts.append(srv_dict)

    return srv_dicts
