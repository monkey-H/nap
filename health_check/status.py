import config
import database
from docker import Client


def container_exists(cli, container_name):
	containers = cli.containers(all=True)
    for k in containers:
        if '/' + container_name in k['Names']:
            return True
    return False

def container_id(username, password, project_name, service_name):
	full_name = username + config.split_mark + project_name + config.split_mark + service_name
	cip = database.machine_ip(username, password, project_name, service_name)

	if cip == '-':
		return False, 'no such project or service'

	cli = Client(base_url=cip, version=config.c_version)

	if container_exists(cli, full_name):
		detail = cli.inspect_container(full_name)
		return True, detail['Id']
	else:
		return False, 'no such container'

def status_id(username, password, project_name, service_name):
	b, id = container_id(username, password, project_name, service_name)
	if b == 'True':
		return True, config.cadvisor_path + '/' + id
	else:
		return False, id

