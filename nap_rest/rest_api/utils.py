# coding: utf-8
import commands
import re


def parse_service_content(raw_content):
    """
    get all services detail and return
    """
    service_record = []
    services = raw_content.split('\n')
    for item in services:
        service_i = {'name': item.split('_')[1]}

        # get url of the service
        status, output = commands.getstatusoutput("nap get_service_url %s" % item)
        if "not found" in output:
            service_i['url'] = '-'
        else:
            service_i['url'] = output

        # get instance num of the service
        status, output = commands.getstatusoutput("nap get_instances_num %s" % item)
        service_i['num'] = output
        service_record.append(service_i)
    return service_record


def parse_app_content(raw_content):
    """
    parse content of instances of specific service
    """
    instances = []
    apps = raw_content.split('\n')

    for item in apps:
        fields = re.split(r'\t+', item)
        inst = {'name': fields[0].split('.')[0].split('_', 1)[1], 'ip': fields[1].split('/')[1], 'active': fields[2],
                'sub': fields[3]}
        instances.append(inst)
    return instances
