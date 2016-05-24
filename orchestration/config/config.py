import os

import yaml  # pip install pyyaml

from docker import Client
from orchestration import schedule
from orchestration import config
from orchestration.database import database_update
from orchestration.exception import ConfigurationError


def table_treat(username, project_name, table):
    services = []
    services_yaml = {}

    for service in table:
        services_yaml[service['name']] = service

    file_path = config.project_path + "/" + username + "/" + project_name + "/nap-compose.yml"
    f = open(file_path, 'w')

    yaml.safe_dump(services_yaml, f)

    for service in table:
        if 'network' not in service:
            service['network'] = username

        if 'ports' in service:
            ports = ['4200']
            for item in service['ports']:
                ports.append(item['container_port'] + ":" + item['host_port'] + ":" + item['protocol'])
            service['ports'] = ports
        else:
            service['ports'] = ['4200']

        if 'volumes' in service:
            volumes = []
            for item in service['volumes']:
                volumes.append(
                    item['container_path'] + ":" + config.project_path + "/" + username + "/" + project_name + item[
                        'host_path'] + ":" + item['mode'])
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

        if 'stateless' not in srv_dict:
            srv_dicts.append(srv_dict)
        elif srv_dict['stateless']:
            scale = int(srv_dict['scale'])
            port = srv_dict['port']
            write_to_ct(str(port), item, project_name, username)

            for i in range(scale):
                srv = {}
                for key in srv_dict:
                    srv[key] = srv_dict[key]

                print srv

                srv['name'] = item + str(i)
                env = []
                if 'environment' in srv:
                    env = srv['environment']

                env.append('SERVICE_NAME=' + item + '-' + project_name + '-' + username)
                srv['environment'] = env

                srv_dicts.append(srv)
        else:
            print (srv_dict['stateless'])

    for srv_dict in srv_dicts:
        if 'network' not in srv_dict:
            srv_dict['network'] = username

        if 'ports' in srv_dict:
            srv_dict['ports'].append('4200')
        else:
            srv_dict['ports'] = ['4200']

        if 'port' in srv_dict:
            srv_dict['ports'].append(srv_dict['port'])

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

    schedule.random_schedule(srv_dicts)

    print srv_dicts

    return srv_dicts


def write_to_ct(port, service_name, project_name, username):
    machines = database_update.get_machines()
    for machine in machines:
        cli = Client(base_url=machine, version=config.c_version)
        tt = cli.exec_create(container='nginx',
                             cmd='/bin/bash -c \"cd /etc/consul-templates && sh refresh.sh %s %s %s %s\"' % (
                                 port, service_name, project_name, username))
        cli.exec_start(exec_id=tt, detach=True)


def delete_from_ct(project_name, username):
    machines = database_update.get_machines()
    for machine in machines:
        cli = Client(base_url=machine, version=config.c_version)
        tt = cli.exec_create(container='nginx',
                             cmd='/bin/bash -c \"cd /etc/consul-templates && bash delete.sh %s-%s\"' % (
                                 project_name, username))
        cli.exec_start(exec_id=tt, detach=True)
