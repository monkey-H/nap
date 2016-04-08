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
        service.cont = Container.get_container_by_name(client, container_name)
        return service

    def create(self):
        if self.cont is not None:
            self.cont.create()

    def start(self):
        if self.cont is not None:
            self.cont.start()

    def stop(self):
        if self.cont is not None:
            self.cont.stop()

    def pause(self):
        if self.cont is not None:
            self.cont.pause()

    def unpause(self):
        if self.cont is not None:
            self.cont.pause()

    def kill(self):
        if self.cont is not None:
            self.cont.kill()

    def remove(self):
        if self.cont is not None:
            self.cont.remove()

    def restart(self):
        if self.cont is not None:
            self.cont.restart()
