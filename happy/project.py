

class Project(object):
    def __init__(self, name, services, client_list):
        self.name = name
        self.service = services
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
