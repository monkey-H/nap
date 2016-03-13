from orchestration.config import config

data = config.read('compose.yml')

for item in data:
	print item
	for key in item:
		print key, 'correspond to', item[key]