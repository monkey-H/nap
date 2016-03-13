
from orchestration.service import Service
from orchestration.config import config
from orchestration import config


class Project(object):
    """
    Represents a project
    contains some services 
    """

    def __init__(self, name, services, client_list):
        self.name = name
        self.services = services
        self.client_list = client_list

    def sort_service_dicts(services):
    # Topological sort (Cormen/Tarjan algorithm).
        unmarked = services[:]
        temporary_marked = set()
        sorted_services = []

        def get_service_names(links):
            return [link.split(':')[0] for link in links]

        def get_service_names_from_volumes_from(volumes_from):
            return [
                parse_volume_from_spec(volume_from).source
                for volume_from in volumes_from
            ]

        def get_service_dependents(service_dict, services):
            name = service_dict['name']
            return [
                service for service in services
                if (name in get_service_names(service.get('links', [])) or
                    name in get_service_names_from_volumes_from(service.get('volumes_from', [])) or
                    name == get_service_name_from_net(service.get('net')))
            ]

        def visit(n):
            if n['name'] in temporary_marked:
                if n['name'] in get_service_names(n.get('links', [])):
                    raise DependencyError('A service can not link to itself: %s' % n['name'])
                if n['name'] in n.get('volumes_from', []):
                    raise DependencyError('A service can not mount itself as volume: %s' % n['name'])
                else:
                    raise DependencyError('Circular import between %s' % ' and '.join(temporary_marked))
            if n in unmarked:
                temporary_marked.add(n['name'])
                for m in get_service_dependents(n, services):
                    visit(m)
                temporary_marked.remove(n['name'])
                unmarked.remove(n)
                sorted_services.insert(0, n)

        while unmarked:
            visit(unmarked[-1])

        return sorted_services

    @classmethod
    def from_dict(cls, username, password, name, service_dicts, client_list):
        project = cls(name, [], client_list)

        for srv_dict in service_dicts:
            if not 'container_name' in srv_dict:
                srv_dict['container_name'] = srv_dict['name']
            srv_dict['hostname'] = username + '-' + name + '-' + srv_dict['container_name']

    	for srv_dict in service_dicts:
            if 'command' in srv_dict:
                command = srv_dict['command']
                if "{{" in command:
    	            for s_dict in service_dicts:
                        before = s_dict['container_name']
                        after = username + "-" + name + "-" + before
                        before = "{{" + before + "}}"
                        command = command.replace(before, after)
    	        srv_dict['command'] = command

        for service_dict in sort_service_dicts(service_dicts):
            log.info('from_dicts service_dict: %s', service_dict)
            if len(l):
                cls.links.append(l);

            #调度算法
            index = random.randint(0,1)
            cc = client_list[index]

            service_dict['volumes_from'] = project.volume
            print project.volume

            log.info(service_dict)

            volumes_from = project.nap_get_volumes_from(service_dict, cc)
            # net = Net(a.get_net())
            # net = project.nap_net(service_dict, username, password)
            net = project.net

            database_update.create_service(username, password, service_dict['container_name'], index, name)

            log.info("===============")

            service_dict['name'] = username + "-" + name + "-" + service_dict['name']
            service_dict['container_name'] = username + "-" + name + "-" + service_dict['container_name']

            if 'ports' in service_dict:
                ports = service_dict['ports']
                if not '4200' in ports:
                    ports.append('4200')
                    service_dict['ports'] = ports
            else:
                ports = []
                ports.append('4200')
                service_dict['ports'] = ports

            log.info(service_dict)

            project.services.append(
                Service(
                    client=cc,
                    project=name,
                    name=service_dict['name']
                    network=net,
                    volume=volumes_from,
                    **service_dict))
        return project

    def from_file(username, password, project_path):
        srv_dicts = config.read()

        if project_path[-1] == '/':
            project_name = project_path.split('/')[-2]
        else:
            project_name = project_path.split('/')[-1]

        return Project.from_dict(username=username, password=password, name=project_name, service_dicts=srv_dicts, client_list=config.client_list)

    def start(self):
        for service in self.services:
            service.start();

    def stop(self):
        for service in self.services:
            service.stop();

    def pause(self):
        for service in self.services:
            service.pause()

    def unpause(self):
        for service in self.services:
            service.unpause()

    def kill(self):
        for service in self.services:
            service.kill()

    def remove(self):
        for service in self.services:
            service.remove()

    def restart(self):
        for service in self.services:
            service.restart()
