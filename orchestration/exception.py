class NoImage(Exception):
	def __init__(self, name):
		self.name = name
		self.msg = "No given image in service: %s" % self.name

	def __str__(self):
		return self.msg

class NoCommand(Exception):
	def __init__(self, name):
		self.name = name
		self.msg = "No given command in service: %s" % self.name

	def __str__(self):
		return self.msg

class ConfigurationError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg