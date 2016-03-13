
from docker import Client

from orchestration.volume import Volume
from orchestration.network import Network

from orchestration.exception import NoImage


class Container(object):
	"""
	Represents a Container
	contains network and volume
	later, some compute resources
	as cpu, memory and so on
	"""

	def __init__(self, client, service, volume=None, network=None, **options):
		self.client = client
		self.service = service
		self.volume = volume
		self.network = network

		self.options = options

	def create(self):
		params = {}

		if not 'image' in self.options:
			raise NoImage(self.service)

		if not 'command' in self.options:
			raise NoCommand(self.service)

		params['image'] = self.options['image']
		params['command'] = self.command
		params['name'] = self.options['container_name']

		if not network == None:
			params['host_config'] = self.client.create_host_config(network_mode=network.name)

		temp_cont = cli.create_container(**params)
		self.id = temp_cont.get('Id')

		self.image = self.options['image']
		self.command = self.options['command']
		self.name = self.options['container_name']


	def start(self):
    	self.client.start(self.id)

    	detail = cli.inspect_container(container = self.id)

    	self.status = detail['State']['Status']
    	self.create_time = detail['Created']
    	self.ip = detail['NetworkSettings']['IPAddress']
    	self.ports = detail['NetworkSettings']['Ports']

    def stop(self):
    	self.client.stop(container=self.name)

    def pause(self):
    	self.client.pause(container=self.name)

    def unpause(self):
    	self.client.unpause(container=self.name)

    def kill(self):
    	self.client.kill(container=self.name)

    def remove(self):
    	self.client.remove_container(container=self.name)

    def restart(self):
    	self.client.restart(container=self.name)
