
class Service(object):
    def __init__(self, name, client, project, network=None, volume=None):
        self.name = name
        self.client = client
        self.project = project
        
