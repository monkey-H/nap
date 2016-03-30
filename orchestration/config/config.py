import yaml
import os
from orchestration.exception import ConfigurationError
import schedule


def read(file_path):
    filename = file_path + '/docker-compose.yml'

    if not os.path.isfile(filename):
        raise ConfigurationError("no docker-compose.yml file found")

    f = open(filename)
    config = yaml.safe_load(f)

    srv_dicts = []

    for item in config:
        srv_dict = {'name': item}
        for key in config[item]:
            srv_dict[key] = config[item][key]
        srv_dicts.append(srv_dict)

    schedule.random_schedule(srv_dicts)
    return srv_dicts
