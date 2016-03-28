from api.container import Container
from api.network import Network
from api.volume import Volume

from api.exception import NoImage

def create_container_test():
    net = Network(name='test', driver='bridge')

    container = Container.create_container(network=net, name='ttttt', url='114.212.87.52:2376', image='ubuntu', command='/bin/sleep 30', version='1.21')
    print container.ip
    print container.cmd
    print container.ports

def create_dict_test():
    url = '114.212.87.52:2376'
    version = '1.21'
    volume = None
    network = None

    dic = {}
    dic['image'] = 'training/webapp'
    dic['container_name'] = 'test'
    # dic['command'] = '/bin/sleep 30'
    dic['hostname'] = 'testhostname'
    dic['mem_limit'] = '24m'
    dic['ports'] = [80, 8000]
    dic['cpu_shares'] = 3

    volume = Volume(['/home/monkey/fuli:/fuli:rw', '/home/monkey/fire:/fire'])
    network = Network('test', 'bridge')
    dic['privileged'] = True

    con = Container(url, version, dic, volume, network)
    con.create()
    con.start()

def create_noimage():
    url = '114.212.87.52:2376'
    version = '1.21'
    volume = None
    network = None

    dic = {}
    dic['container_name'] = 'test'

    con = Container(url, version, dic, volume, network)
if __name__ == '__main__':
    try:
        create_dict_test()
    except NoImage as e:
        print e.msg
