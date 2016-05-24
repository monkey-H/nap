from orchestration.database import database_update
import random


def random_schedule(service_list):
    machines = database_update.get_machines()
    for service in service_list:
        if 'host' not in service:
            index = random.randint(0, len(machines)-1)
            print index
            machine = database_update.get_machine(index)
            service['host'] = machine
    return service_list
