from orchestration.database import database_update
import random


def random(service_list):
    machines = database_update.get_machines()
    for service in service_list:
        if 'host' not in service:
            index = random.randint(0, machines)
            machine = database_update.get_machine(index)
            service['host'] = machine
    return service_list
