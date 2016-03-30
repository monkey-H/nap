# nap-py: 容器引擎接口
----

该项目希望综合docker，rkt，lxc/lxd及runC等容器相关开源项目中关于容器引擎，计算，存储，网络资源的语义，为nap-core项目提供一个比较稳定和统一的抽象接口。
我们不追求完全实现上述项目中的所有特性。
自顶向下，从上层组件的需求出发，结合现有容器开源项目已实现的功能，来设计这个接口。
由于docker的发展和功能要比其它项目更成熟，所以目前主要以docker为基础，基于`docker-py`来实现。

项目使用python 2开发，依赖的`docker-py`，可通过pip来安装
```
sudo pip install docker-py
```

## 参考文档
+ [Docker Restful API v1.22](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.22/)
+ [docker-py doc](http://docker-py.readthedocs.org/en/stable/)
+ [rkt Doc](https://github.com/coreos/rkt/blob/master/Documentation/commands.md)
+ [lxc Doc](https://linuxcontainers.org/lxc/documentation/#python)
+ [runC](https://github.com/opencontainers/runc)

+ [rkt vs. others](https://coreos.com/rkt/docs/latest/rkt-vs-other-projects.html)

### container create options

+ image: the image to run
+ command: the command to be run in the container
+ hostname: optional hostname for container
+ mem_limit(float or str): memory limit(format: [number][optional unit] where unit = b,k,m, or g)
+ ports: a list of port numbers
+ environment(dict or list): A dictionary or a list of strings in the following format ["password=xxx" or {"password": "xxx"}
+ dns(list): dns name servers
+ name: a name for the container
+ entrypoint: an entrypoint
+ cpu_shares(int): cpu shares(relative weight)
+ working_dir: path to working directory
+ domainname: set custom DNS search domains
+ memswap_limit(int):
+ host_config: a hostconfig directory
+ mac_address(str): the mac address to assign the container
+ labels(dict or list): a dictionary of name-value labels({"label1": "value1", "label2": "value2"}) or a list of names of labels to set with empty values(["label1", "label2"])

+ volumes(str or list):
+ volumes_from (str or list): list of container names or Ids to get volumes from. Optionally a single string joining container id's with commas
+ network_disable(bool): disable networking

### container host_config

+ port bindings  cli.create_host_config(port_bindings={container_port:host_port, 222: None})
+ host_config=cli.create_host_config(port_bindings={111:4567, 222: None})
+ limit the host address on which the port will be exposed:
    cli.create_host_config(port_bindings={1111: ('127.0.0.1', 4567)})
+ without host port assignment:
    cli.create_host_config(port_bindings={1111: ('127.0.0.1',)})
+ use UDP instead of TCP(default)
    container_id = cli.create_container(
    'busybox', 'ls', ports=[(1111, 'udp'), 2222],
    host_config=cli.create_host_config(port_bindings={
        '1111/udp': 4567, 2222: None
    })
    )
+ bind several ips to the same port
    cli.create_host_config(port_bindings={
    1111: [
        ('192.168.0.100', 1234),
        ('192.168.0.101', 1234)
    ]
    })
+ single container port to several host ports:
    cli.create_host_config(port_bindings={111: [2345,6789]})

### using volumes

+ Volume declaration is done in two parts. Provide a list of mountpoints to the Client().create_container() method, and declare mappings in the host_config section.
    container_id = cli.create_container(
    'busybox', 'ls', volumes=['/mnt/vol1', '/mnt/vol2'],
    host_config=cli.create_host_config(binds={
        '/home/user1/': {
            'bind': '/mnt/vol2',
            'mode': 'rw',
        },
        '/var/www': {
            'bind': '/mnt/vol1',
            'mode': 'ro',
        }
    })
    )

+  container_id = cli.create_container(
    'busybox', 'ls', volumes=['/mnt/vol1', '/mnt/vol2'],
    host_config=cli.create_host_config(binds=[
        '/home/user1/:/mnt/vol2',
        '/var/www:/mnt/vol1:ro',
    ])
    )

### using Networks

+  host_config=cli.create_host_config(network_mode=network.name)

### host configuration

+ binds: Volumes to bind. See Using volumes for more information.
+ port_bindings (dict): Port bindings. See Port bindings for more information.
+ lxc_conf (dict): LXC config
+ privileged (bool): Give extended privileges to this container
+ links (dict or list of tuples): either as a dictionary mapping name to alias or as a list of (name, alias) tuples
+ dns (list): Set custom DNS servers
+ restart_policy (dict): "Name" param must be one of  ['on-failure', 'always']
+ network_mode (str): One of ['bridge', 'none', 'container:<name|id>', 'host']


+ oom_kill_disable (bool): Whether to disable OOM killer
+ publish_all_ports (bool): Whether to publish all ports to the host
+ dns_search (list): DNS search domains
+ volumes_from (str or list): List of container names or Ids to get volumes from. Optionally a single string joining container id's with commas
+ cap_add (list of str): Add kernel capabilities
+ cap_drop (list of str): Drop kernel capabilities
+ extra_hosts (dict): custom host-to-IP mappings (host:ip)
+ read_only (bool): mount the container's root filesystem as read only
+ pid_mode (str): if set to "host", use the host PID namespace inside the container
+ ipc_mode (str): Set the IPC mode for the container
+ security_opt (list): A list of string values to customize labels for MLS systems, such as SELinux.
+ ulimits (list): A list of dicts or docker.utils.Ulimit objects. A list of ulimits to be set in the container.
+ log_config (docker.utils.LogConfig or dict): Logging configuration to container
+ mem_limit (str or int): Maximum amount of memory container is allowed to consume. (e.g. '1G')
+ memswap_limit (str or int): Maximum amount of memory + swap a container is allowed to consume.
+ mem_swappiness (int): Tune a container's memory swappiness behavior. Accepts number between 0 and 100.
+ shm_size (str or int): Size of /dev/shm. (e.g. '1G')
+ cpu_group (int): The length of a CPU period in microseconds.
+ cpu_period (int): Microseconds of CPU time that the container can get in a CPU period.
+ group_add (list): List of additional group names and/or IDs that the container process will run as.
+ devices (list): Host device bindings. See host devices for more information.


###volume operations   
+ 可以创建卷容器，可以挂载到这个容器上　　
+ 用户如果想制定某一个容器挂载到某一个特殊路径下，在create阶段指定　　
+ 卷容器，不可以指定挂载到某一个路径下，只能是默认路径/var/lib/docker/volume
+ nap使用过程中，可以把特定用户的ｍｆｓ路径作为前缀，每次要挂载路径的时候，指定就好　　
