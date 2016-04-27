import os

import yaml #pip install pyyaml

from orchestration import schedule
from orchestration import config
from orchestration.exception import ConfigurationError


def table_treat(username, project_name, table):
    services = []

    for service in table:
        if 'network' not in service:
            service['network'] = username

        if 'ports' in service:
            ports = [4200]
            for item in service['ports']:
                ports.append(item['container_port'] + ":" + item['host_port'] + ":" + item['protocol'])
            service['ports'] = ports
        else:
            service['ports'] = [4200]

        if 'volumes' in service:
            volumes = []
            for item in service['volumes']:
                volumes.append(item['container_path'] + ":" + config.project_path + "/" + username + "/" + project_name + item['host_path'] + ":" + item['mode'])
            service['volumes'] = volumes

        services.append(service)

    schedule.random_schedule(services)

    return services


def read(file_path, username, project_name):
    filename = file_path + '/nap-compose.yml'

    if not os.path.isfile(filename):
        raise ConfigurationError("no nap-compose.yml file found")

    f = open(filename)
    configs = yaml.safe_load(f)

    srv_dicts = []

    for item in configs:
        srv_dict = {'name': item}
        for key in configs[item]:
            srv_dict[key] = configs[item][key]

        if 'network' not in srv_dict:
            srv_dict['network'] = username

        if 'ports' in srv_dict:
            srv_dict['ports'].append(4200)
        else:
            srv_dict['ports'] = [4200]

        if 'volumes' in srv_dict:
            new_volumes = []
            for volume in srv_dict['volumes']:
                items = volume.split(":")
                if len(items) == 1:
                    new_volumes.append(volume)
                    continue
                else:
                    items[1] = config.project_path + "/" + username + "/" + project_name + items[1]
                new_volume = items[0] + ":" + items[1]
                if len(items) == 3:
                    new_volume = new_volume + ":" + items[2]

                new_volumes.append(new_volume)

            srv_dict['volumes'] = new_volumes

        srv_dicts.append(srv_dict)

    schedule.random_schedule(srv_dicts)
    return srv_dicts
