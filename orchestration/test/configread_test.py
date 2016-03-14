from orchestration.config import config
import sys

if __name__ == '__main__':
	print sys.path[0]
	data = config.read(sys.path[0])

	for item in data:
		print item
		for key in item:
			print key, 'correspond to', item[key]
