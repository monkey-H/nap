from orchestration.nap_api.project_create import create_project_from_table

table = []
t = {}
t['name'] = 'master'
t['cpu_shares'] = '1024'
t['mem_limit'] = '32m'
t['command'] = '/usr/sbin/sshd -D'
t['image'] = 'docker.iwanna.xyz:5000/hmonkey/mpi:v1'
t['volumes'] = [{'container_path': '/data', 'host_path': '/va', 'mode': 'rw'}, {'container_path': '/datass', 'host_path': '/vagr', 'mode': 'ro'}]
t['ports'] = [{'container_port': '3200', 'host_port': '32400', 'protocol': 'tcp'}, {'container_port': '3300', 'host_port': '32401', 'protocol': 'udp'}]
table.append(t)

t = {}
t['name'] = 'slave'
t['cpu_shares'] = '1024'
t['mem_limit'] = '32m'
t['command'] = '/usr/sbin/sshd -D'
t['image'] = 'docker.iwanna.xyz:5000/hmonkey/mpi:v1'
t['volumes'] = [{'container_path': '/data', 'host_path': '/va', 'mode': 'rw'}, {'container_path': '/datass', 'host_path': '/vagr', 'mode': 'ro'}]
t['ports'] = [{'container_port': '3200', 'host_port': '32400', 'protocol': 'tcp'}, {'container_port': '3300', 'host_port': '32401', 'protocol': 'udp'}]
table.append(t)

print create_project_from_table('bana', 'tabless', table)
