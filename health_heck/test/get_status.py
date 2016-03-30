#!/usr/bin/python

import time
import consul
import health_heck.config


def get_status(user_name, project_name, service_name):
    c = consul.Consul(health_heck.config.consul_url)

    v = c.kv.get('nap_services/%s/%s/%s' % (user_name, project_name, service_name))
    print(v)
    # ('20083369', {u'LockIndex': 0, u'ModifyIndex': 20083369,
    #               u'Value':
    #                       "{'status': u'Up 3 weeks',
    #                         'name': 'MongoRouter',
    #                         'time': 1453871253.918488}",
    #               u'Flags': 0,
    #               u'Key': u'nap_services/apple/iii/MongoRouter',
    #               u'CreateIndex': 2956159
    #               }
    # )

    vv = eval(v[1]['Value'])  # Convert string to dictionary
    print time.time() - vv['time']


get_status('monkey', 'wwww', 'web')
# print c.kv.put('test/hello', 'world')
# c.kv.put('test/world', 'world')
# print c.kv.get('test/hello')
# print c.kv.get('test/world')
# c.kv.delete('test', recurse=True)
# print c.kv.get('test/hello')
# print c.kv.get('test/world')
