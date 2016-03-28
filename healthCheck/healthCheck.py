#!/usr/bin/python

import time
import sys
import consul
from docker import Client

TIME_GAP = 5

def updateStatus():
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
        time.sleep(TIME_GAP)

if __name__ == "__main__":
    updateStatus()
