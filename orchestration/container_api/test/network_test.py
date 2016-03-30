from api.network import Network
from docker import Client

cli = Client(base_url='114.212.87.52:2376', version='1.21')
Network.create_network(cli, 'test', 'bridge')

net = Network(name='test', driver='bridge')
