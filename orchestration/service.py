from orchestration.container_api.container import Container


class Service(object):
    """
    Represents a service
    contains some containers
    now only one
    """

    def __init__(self, name, client, project, network=None, volume=None, options=None):
        print options
        self.name = name
        self.client = client
        self.project = project
        self.cont = Container(client=client, network=network, volume=volume, options=options)

    @classmethod
    def get_service_by_name(cls, name, client, project, container_name):
        service = Service(name, client, project)
        service.cont = Container.getContainerByName(client, container_name)
        return service

    def create(self):
        self.cont.create()

    def start(self):
        self.cont.start()

    def stop(self):
        self.cont.stop()

    def pause(self):
        self.cont.pause()

    def unpause(self):
        self.cont.pause()

    def kill(self):
        self.cont.kill()

    def remove(self):
        self.cont.remove()

    def restart(self):
        self.cont.restart()
