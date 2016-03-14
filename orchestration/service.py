from orchestration.container import Container

class Service(object):
	"""
	Represents a service
	contains some containers
	now only one
	"""

	def __init__(self, name, client, project, network=None, volume=None, **options):
		self.name = name
		self.client = client
		self.project = project
		self.cont = Container(client=client, service=name, network=network, volume=volume, **options)

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
