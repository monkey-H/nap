# -*- coding: utf-8 -*-


from docker.errors import NotFound
from docker.errors import APIError
from exception import NoImage
from exception import StatusError

import config
from network import Network
from image import Image

import logging as log


class Container(object):
    """
    Wraps a Docker container
    """

    def __init__(self, client, options, volume=None, network=None):
        self.client = client.client
        self.volume = volume
        self.network = network

        self.options = options

        self.ip = None
        self.id = None
        self.full_name = None
        self.user_name=None
        self.project_name=None
        self.service_name=None
        self.status = None
        self.image = None
        self.cmd = None
        self.create_time = None
        self.ports = None

    @classmethod
    def get_container_by_name(cls, client, name):
        cli = client.client

        containers = cli.containers(all=True)
        for item in containers:
            if '/' + name in item['Names']:
                detail = cli.inspect_container(item['Id'])

                network_name = detail['HostConfig']['NetworkMode']

                if not network_name == "default":
                    network_detail = cli.inspect_network(network_name)
                    network_driver = network_detail['Driver']
                    network = Network(network_name, network_driver)
                else:
                    network = None
                volume = None

                con = Container(client, None, volume, network)

                con.ip = detail['NetworkSettings']['IPAddress']
                con.id = item['Id']
                con.name = name
                con.status = item['Status']
                con.image = item['Image']
                con.cmd = item['Command']
                con.create_time = item['Created']
                con.ports = {}
                for port in item['Ports']:
                    if 'PublicPort' in port:
                        con.ports[str(port['PrivatePort'])] = port['PublicPort']
                    else:
                        con.ports[str(port['PrivatePort'])] = '-'

                return con

        return None

    @classmethod
    def _parse_container_name(cls, full_name):
        """
        :param full_name: svc-num.prj.user
        :return:
        """
        names=str(full_name).split(config.container_name_separator)
        if not len(names) == 3:
            log.warning("Bad formatted container name:[%s] " % full_name)
            return None
        else:
            return names

    @classmethod
    def _join_container_name(cls, service, project, user):
        return config.container_name_separator.join([service, project, user])

    def exists(self, name):
        cli = self.client
        containers = cli.containers(all=True)
        for item in containers:
            if '/' + name in item['Names']:
                return True
        return False

    def create(self):
        params = {}

        if 'image' not in self.options:
            raise NoImage('Container does not contain image')

        # params['image'] = Image(self.client, self.options['image'])
        params['image'] = self.options['image']
        self.image = Image(self.client, params['image'])

        if 'command' in self.options:
            params['command'] = self.options['command']

        mem_limit = None
        if 'mem_limit' in self.options:
            # params['mem_limit'] = self.options['mem_limit']
            mem_limit = self.options['mem_limit']

        # ports binding need
        port_bindings = None
        if 'ports' in self.options:
            params['ports'] = self.options['ports']
            port_bindings = {}
            for item in self.options['ports']:
                port_bindings[item] = None

        if 'hostname' in self.options:
            params['hostname'] = self.options['hostname']

        if 'environment' in self.options:
            params['environment'] = self.options['environment']

        if 'dns' in self.options:
            params['dns'] = self.options['dns']

        if 'entrypoint' in self.options:
            params['entrypoint'] = self.options['entrypoint']

        if 'cpu_shares' in self.options:
            params['cpu_shares'] = self.options['cpu_shares']

        if 'container_name' in self.options:
            params['name'] = self.options['container_name']

        if 'working_dir' in self.options:
            params['working_dir'] = self.options['working_dir']

        if 'domainname' in self.options:
            params['domainname'] = self.options['domainname']

        if 'mac_address' in self.options:
            params['mac_address'] = self.options['mac_address']

        network_mode = None
        if self.network is not None:
            network_mode = self.network.name

        binds = None
        if self.volume is not None:
            binds = self.volume.vol

        privileged = False
        if 'privileged' in self.options:
            privileged = self.options['privileged']

        # todo -v 挂载volume
        # todo 注意：vol只能在创建容器的时候制定，不像network那样既可以创建时指定也可以启动后attach

        volumes_from = None
        if 'volumes_from' in self.options:
            volumes_from = self.options['volumes_from']

        print(port_bindings)
        params['host_config'] = self.client.create_host_config(port_bindings=port_bindings, network_mode=network_mode,
                                                               binds=binds, privileged=privileged,
                                                               volumes_from=volumes_from, mem_limit=mem_limit)

        container = self.client.create_container(**params)

        self.id = container.get('Id')

    def start(self):
        # todo 是否先检查容器是否已经create了？
        try:
            self.client.start(container=self.id)
        except NotFound as e:
            raise StatusError(e.explanation)

        detail = self.client.inspect_container(container=self.id)

        self.name = detail['Name']
        self.status = detail['State']['Status']

        command = ""
        for item in detail['Config']['Cmd']:
            command = command + item + " "
        self.cmd = command

        self.create_time = detail['Created']
        self.ip = detail['NetworkSettings']['IPAddress']
        self.ports = detail['NetworkSettings']['Ports']

    def stop(self):
        self.client.stop(container=self.id)

    def pause(self):
        self.client.pause(container=self.id)

    def unpause(self):
        self.client.unpause(container=self.id)

    def kill(self):
        self.client.kill(container=self.id)

    def remove(self):
        self.client.remove_container(container=self.id)

    def restart(self):
        self.client.restart(container=self.id)

    def attachToNetwork(self, net_name):
        detail = self.client.inspect_network(net_name)
        self.attachToNetworkByID(detail['Id'])

    def attachToNetworkByID(self, netID):
        try:
            self.client.connect_container_to_network(self.id, netID)
        except APIError as e:
            raise StatusError(e.explanation)
