# coding=utf-8
from docker import Client as dockerClient


class Client(object):
    """
    Docker engine client
    """
    def __init__(self, host_url, version="auto"):
        self.client = dockerClient(base_url=host_url, version=version)
        self.host_url = host_url
        self.version = version

    def get_host_url(self):
        return self.host_url

    def get_version(self):
        return self.version

    def get_running_containers(self):
        containers = self.client.containers(all=False)
        # todo 从 docker-py 的 container 转换到自定义的 container
        return containers

    def get_all_containers(self):
        containers = self.client.containers(all=True)
        # todo 从 docker-py 的 container 转换到自定义的 container
        return containers

    @classmethod
    def get_local_client(cls):
        return Client('127.0.0.1:2376')

