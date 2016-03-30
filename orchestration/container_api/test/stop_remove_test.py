from api.container import Container
from api.volume import Volume
from api.network import Network
from api.client import Client
import time

def create_test():
    url = '114.212.87.52:2376'
    version = '1.21'
    volume = None
    network = None

    client = Client(url, version)

    dic = {}
    dic['image'] = 'training/webapp'
    # dic['container_name'] = 'test'
    # dic['command'] = '/bin/sleep 30'
    dic['hostname'] = 'testhostname'
    dic['mem_limit'] = '24m'
    dic['ports'] = [80, 8000]
    dic['cpu_shares'] = 3

    volume = Volume(['/home/monkey/fuli:/fuli:rw', '/home/monkey/fire:/fire'])
    network = Network('test', 'bridge')
    dic['privileged'] = True

    con = Container(client, dic, volume, network)
    con.create()
    return con

def start_test(container):
    container.start()

def pause_test(container):
    container.pause()

def unpause_test(container):
    container.unpause()

def kill_test(container):
    container.kill()

def restart_test(container):
    container.restart()

def stop_test(container):
    container.stop()

def remove_test(container):
    container.remove()

if __name__ == "__main__":
    con = create_test()
    print con.id
    start_test(con)

    time.sleep(5)

    # pause_test(con)
    # unpause_test(con)
    # restart_test(con)
    # # stop_test(con)
    # kill_test(con)
    # remove_test(con)
