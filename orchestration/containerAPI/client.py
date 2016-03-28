from docker import Client as docker_client

class Client(object):
    '''
    Docker engine client
    '''
    def __init__(self, hostURL, version):
        self.client = docker_client(base_url=hostURL, version=version)
        self.url = hostURL
        self.version = version

    def get_url(self):
        return self.url

    def get_version(self):
        return self.version
