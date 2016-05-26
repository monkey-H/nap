# coding=utf-8

from orchestration.database import database_update
from orchestration.nap_api import app_info
from orchestration.container_api.client import Client
from orchestration.container_api.container import Container
from orchestration import config


def service_load_calculate(username, project_name, service_name):
    usages = app_info.container_monitor(username, project_name, service_name)
    current_usage = {'cpu': usages[-1]['cpu'],
                     'memory': usages[-1]['memory']}

    return current_usage


def scale_up(username, project_name, service_name, service_dict):
    ip = service_dict['host']
    client = Client(ip, config.c_version)
    service_dict['container_name'] = service_name + "." + project_name + "." + username
    cont = Container(client=client, options=service_dict, volume=None, network=service_dict['network'])
    cont.create()
    cont.start()
    database_update.create_service(username, service_name, ip, project_name)
    # TODO check does consul-templates reload nginx successfully


def scale_down(username, project_name, service_name):
    full_name = service_name + "." + project_name + "." + username
    ip = database_update.service_ip(username, project_name, service_name)
    client = Client(ip, config.c_version)
    cont = Container.get_container_by_name(client, full_name)
    cont.stop()
    cont.remove()
    database_update.delete_service(username, project_name, service_name)
