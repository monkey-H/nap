import yaml
import os
from orchestration.exception import ConfigurationError

def read(file_path):

	file = file_path + '/docker-compose.yml'

	if not os.path.isfile(file):
		raise ConfigurationError("no docker-compose.yml file found")

	f = open(file)
	config = yaml.safe_load(f)

	srv_dicts = []

	for item in config:
		srv_dict = {}
		srv_dict['name'] = item
		for key in config[item]:
			srv_dict[key] = config[item][key]
		srv_dicts.append(srv_dict)

	return srv_dicts
