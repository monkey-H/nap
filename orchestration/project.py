from orchestration.service import Service
from orchestration.config import config as file_treat
from orchestration import config
from orchestration.exception import ConfigError

from orchestration.exception import DependencyError
from orchestration.database import database_update

import logging
import random
from container_api.client import Client

log = logging.getLogger(__name__)


def parse_volume_from_spec(volume_from_config):
    parts = volume_from_config.split(':')
    if len(parts) > 2:
        raise ConfigError("Volume %s has incorrect format, should be "
                          "external:internal[:mode]" % volume_from_config)

    if len(parts) == 1:
        source = parts[0]
        mode = 'rw'
    else:
        source, mode = parts

    return source


def sort_service_dicts(services):
    # Topological sort (Cormen/Tarjan algorithm).
    unmarked = services[:]
    temporary_marked = set()
    sorted_services = []

    def get_service_name_from_net(net_config):
        if not net_config:
            return

        if not net_config.startswith('container:'):
            return

        _, net_name = net_config.split(':', 1)
        return net_name

    def get_service_names(links):
        return [link.split(':')[0] for link in links]

    def get_service_names_from_volumes_from(volumes_from):
        return [
            parse_volume_from_spec(volume_from)
            for volume_from in volumes_from
            ]

    def get_service_dependents(service_dict, srv):
        name = service_dict['name']
        return [
            service for service in srv
            if (name in get_service_names(service.get('links', [])) or
                name in get_service_names_from_volumes_from(service.get('volumes_from', [])) or
                name == get_service_name_from_net(service.get('net')))
            ]

    def visit(n):
        if n['name'] in temporary_marked:
            if n['name'] in get_service_names(n.get('links', [])):
                raise DependencyError('A service can not link to itself: %s' % n['name'])
            if n['name'] in n.get('volumes_from', []):
                raise DependencyError('A service can not mount itself as volume: %s' % n['name'])
            else:
                raise DependencyError('Circular import between %s' % ' and '.join(temporary_marked))
        if n in unmarked:
            temporary_marked.add(n['name'])
            for m in get_service_dependents(n, services):
                visit(m)
            temporary_marked.remove(n['name'])
            unmarked.remove(n)
            sorted_services.insert(0, n)

    while unmarked:
        visit(unmarked[-1])

    return sorted_services


class Project(object):
    """
    Represents a project
    contains some services
    """

    def __init__(self, name, services):
        self.name = name
        self.services = services

    @classmethod
    def from_dict(cls, username, name, service_dicts):
        project = cls(name, [])

        for srv_dict in service_dicts:
            if 'container_name' not in srv_dict:
                srv_dict['container_name'] = srv_dict['name']
            srv_dict['hostname'] = username + '-' + name + '-' + srv_dict['container_name']

        for srv_dict in service_dicts:
            if 'command' in srv_dict:
                command = srv_dict['command']
                if "{{" in command:
                    for s_dict in service_dicts:
                        before = s_dict['container_name']
                        after = username + "-" + name + "-" + before
                        before = "{{" + before + "}}"
                        command = command.replace(before, after)
                srv_dict['command'] = command

        for service_dict in sort_service_dicts(service_dicts):
            log.info('from_dicts service_dict: %s', service_dict)

            container_name = service_dict['container_name']
            service_dict['name'] = service_dict['name'] + config.split_mark + name + config.split_mark + username
            service_dict['container_name'] = service_dict['container_name'] + config.split_mark + name + config.split_mark + username
            # service_dict['name'] = username + "-" + name + "-" + service_dict['name']
            # service_dict['container_name'] = username + "-" + name + "-" + service_dict['container_name']
            # print service_dict

            # service_dict['name'] = username + "-" + name + "-" + service_dict['name']
            # service_dict['container_name'] = username + "-" + name + "-" + service_dict['container_name']

            if 'ports' in service_dict:
                ports = service_dict['ports']
                if '4200' not in ports:
                    ports.append('4200')
                    service_dict['ports'] = ports
            else:
                ports = ['4200']
                service_dict['ports'] = ports

            log.info(service_dict)

            print service_dict

            client_list = database_update.get_machines()

            if 'host' in service_dict:
                if service_dict['host'] == 'all':
                    no = 0
                    for client in client_list:
                        cc = Client(client, config.c_version)
                        project.services.append(
                            Service(
                                name=service_dict['name'],
                                client=cc,
                                project=name,
                                network=None,
                                volume=None,
                                options=service_dict
                            )
                        )
                        database_update.create_service(username, container_name+no, client, name)
                        no += 1
                    return project
                else:
                    ip = service_dict['host']
            else:
                # orchestration algorithm
                # index = random.randint(0, 1)
                print 'no schedule'

            cc = Client(ip, config.c_version)

            project.services.append(
                Service(
                    name=service_dict['name'],
                    client=cc,
                    project=name,
                    network=None,
                    volume=None,
                    options=service_dict))

            database_update.create_service(username, container_name, ip, name)
        return project

    @classmethod
    def from_file(cls, username, project_path):
        srv_dicts = file_treat.read(project_path)

        if project_path[-1] == '/':
            project_name = project_path.split('/')[-2]
        else:
            project_name = project_path.split('/')[-1]

        return cls.from_dict(username=username, name=project_name, service_dicts=srv_dicts)

    @classmethod
    def get_project_by_name(cls, project_name, service_list):
        project = Project(project_name, [])
        for service in service_list:
            service_name = service['name']
            service_ip = service['ip']

            cli = Client(service_ip, config.c_version)

            project.services.append(
                Service.get_service_by_name(service_name, cli, project_name, service_name)
            )
        return project

    def create(self):
        for service in self.services:
            service.create()

    def start(self):
        for service in self.services:
            service.start()

    def stop(self):
        for service in self.services:
            service.stop()

    def pause(self):
        for service in self.services:
            service.pause()

    def unpause(self):
        for service in self.services:
            service.unpause()

    def kill(self):
        for service in self.services:
            service.kill()

    def remove(self):
        for service in self.services:
            service.remove()

    def restart(self):
        for service in self.services:
            service.restart()
