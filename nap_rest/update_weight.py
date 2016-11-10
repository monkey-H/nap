from docker import Client

from .orchestration.nap_api import app_info

def get_container_load(username, project_name, service_name, container_name):
    usage = app_info.container_resource_usage(username, project_name, service_name, container_name)

    if usage is None:
        return

    cpu_usage = usage["cpu_usage"]
    mem_usage = usage["mem_usage"]

    cpu_weight = int((1-cpu_usage)*10)
    mem_weight = int((1-mem_usage)*10)

    weight = cpu_weight
    if (cpu_weight > mem_weight):
        weight = mem_weight

    return weight


def
