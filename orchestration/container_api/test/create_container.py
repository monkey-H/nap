from api.container import Container

container = Container.create_container(url='114.212.87.52:2376', image='ubuntu', command='/bin/sleep 30', version='1.21')
print container.ip
print container.cmd
print container.ports
