#!/usr/bin/python

from docker import Client
import consul
import time

TIME_GAP = 10

#!/usr/bin/python

import time
import sys
import consul
from docker import Client

def update_status():
    c = consul.Consul(host=sys.argv[1])
    cli = Client(base_url=sys.argv[1]+':2376', version='1.21')
    while 1:
        containers = cli.containers(all=True)
        for container in containers:
            full_name = str(container['Names'][0]).split('/')[1]
            if not len(str(full_name).split('-')) == 3:
                continue
            user_name = str(full_name).split('-')[0]
            project_name = str(full_name).split('-')[1]
            service_name = str(full_name).split('-')[2]
            value={}
            value['name'] = service_name
            value['status'] = container['Status']
            value['time'] = time.time()
            c.kv.put('nap_services/%s/%s/%s' % (user_name, project_name, service_name), str(value))
            print  c.kv.get('nap_services/%s/%s/%s' % (user_name, project_name, service_name))
        time.sleep(TIME_GAP)

def get_status(user_name, project_name, service_name):
    c = consul.Consul(host='114.212.189.147')
    value = c.kv.get('nap_services/%s/%s/%s' % (user_name, project_name, service_name))[1]
    vv = eval(value['Value'])
    update_time = vv['time']
    current_time = time.time()
    update_gap = current_time - update_time
    print update_gap
    if (update < TIME_GAP):
        return vv['status']
    else:
        return 'not update for long time'


get_status('monkey', 'wwww', 'web')
# print c.kv.put('test/hello', 'world')
# c.kv.put('test/world', 'world')
# print c.kv.get('test/hello')
# print c.kv.get('test/world')
# c.kv.delete('test', recurse=True)
# print c.kv.get('test/hello')
# print c.kv.get('test/world')
