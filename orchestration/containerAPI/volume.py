from docker import Client
from docker.errors import NotFound


class Volume(object):
    """
    Represents a volume in nap
    """

    # vol is a list ['host_path:container/path:rw', '/home:/var:ro']
    def __init__(self, vol):
        self.vol = vol

    @classmethod
    def create(cls, url, version, name, driver='local'):
        cli = Client(base_url=url, version=version)
        cli.create_volume(name=name, driver=driver)

    @classmethod
    def remove(cls, url, version, name):
        cli = Client(base_url=url, version=version)
        try:
            cli.remove_volume(name=name)
        except NotFound as e:
            return 'No such volume'
        except:
            return 'Error happened when remove volume: %s' % name

        return 'Succeed'

    @classmethod
    def inspect(cls, url, version, name):
        cli = Client(base_url=url, version=version)
        dic = cli.inspect_volume(name)
        return dic

    @classmethod
    def lists(cls, url, version):
        cli = Client(base_url=url, version=version)
        items = cli.volumes()
        return items
