from orchestration.container_api.container import Container
from orchestration.database import database_update
from orchestration.container_api.client import Client
from orchestration import config
from orchestration import schedule


def write_to_ct(port, service_name, project_name, username):
    machines = database_update.get_machines()
    for machine in machines:
        cli = Client(machine, config.c_version).client
        tt = cli.exec_create(container='nginx',
                             cmd='/bin/bash -c \"cd /etc/consul-templates && sh refresh.sh %s %s %s %s\"' % (
                                 port, service_name, project_name, username))
        cli.exec_start(exec_id=tt, detach=True)


def delete_from_ct(project_name, username):
    machines = database_update.get_machines()
    for machine in machines:
        cli = Client(machine, config.c_version).client
        tt = cli.exec_create(container='nginx',
                             cmd='/bin/bash -c \"cd /etc/consul-templates && bash delete.sh %s-%s\"' % (
                                 project_name, username))
        cli.exec_start(exec_id=tt, detach=True)


class Service(object):
    """
    Represents a service
    contains some containers
    now only one
    """

    def __init__(self, name, project, username, network=None, volume=None, options=None):
        print options
        self.name = name
        self.project = project
        self.username = username
        self.containers = []

        if options is not None:
            scale = options['scale']

            for i in range(int(scale)):
                option = {}
                for item in options:
                    option[item] = options[item]

                ip = schedule.random_schedule()

                client = Client(ip, config.c_version)
                option['container_name'] = name + "_" + str(i) + config.split_mark + project + config.split_mark + username
                option['hostname'] = name + "_" + str(i) + config.split_mark + project + config.split_mark + username
                cont = Container(client=client, network=network, volume=volume, options=option)

                database_update.create_container(username, project, name, name + "_" + str(i), ip)
                self.containers.append(cont)

    @classmethod
    def get_service_by_name(cls, username, project_name, service_name):
        service = Service(service_name, project_name, username)

        container_list = database_update.container_list(username, project_name, service_name)

        print 'container_list'
        print container_list

        for container_name in container_list:
            full_name = container_name[0] + config.split_mark + project_name + config.split_mark + username
            ip = database_update.container_ip(username, project_name, service_name, container_name[0])
            client = Client(ip, config.c_version)
            cont = Container.get_container_by_name(client, full_name)
            service.containers.append(cont)

        return service

    def create(self):
        for cont in self.containers:
            if cont is not None:
                cont.create()

    def start(self):
        for cont in self.containers:
            if cont is not None:
                cont.start()
                tt = cont.client.exec_create(container=cont.name, cmd='shellinaboxd -t -b')
                cont.client.exec_start(exec_id=tt, detach=True)

                ttt = cont.client.exec_create(container=cont.name,
                                                      cmd='/bin/bash -c \"useradd admin && echo -e \\\"admin\\\\nadmin\\\" | passwd admin\"')
                cont.client.exec_start(exec_id=ttt, detach=True, stream=True, tty=True)

    def stop(self):
        for cont in self.containers:
            if cont is not None:
                cont.stop()

    def pause(self):
        for cont in self.containers:
            if cont is not None:
                cont.pause()

    def unpause(self):
        for cont in self.containers:
            if cont is not None:
                cont.pause()

    def kill(self):
        for cont in self.containers:
            if cont is not None:
                cont.kill()

    def remove(self):
        # TODO remove from consul-template
        delete_from_ct(self.project, self.username)
        for cont in self.containers:
            if cont is not None:
                cont.remove()

    def restart(self):
        for cont in self.containers:
            if cont is not None:
                cont.restart()
