# nap-core： 跨主机多容器应用编排和部署方案。

2016-03-11

## 组件：
+ docker：容器引擎，运行在 **每台** 主机上。
+ consul：高可用的键值存储，用来支持 docker（v1.9+） 的 overlay 网络及其它系统信息，运行在 **每台** 主机上。由于v1.10之前的 `docker daemon` 在每台主机上只有单个运行进程，所以 `consul` 作为主机进程而不是容器来执行。
+ moosefs：分布式存储组件，使用 `mfs_chunkserver` 容器，运行在 **每台** 主机上，用来统一管理集群中各个主机的存储空间。
+ database：数据库组件，使用 `mysql` 数据库容器，用来存储用户基本信息，应用列表等信息，运行在 **主节点** 上。
+ security_certificate：安全认证组件，通过 `ldap` ，实现用户的认证管理，运行在 **主节点** 上。
+ orchestration：容器编排和部署控制组件，通过改写 `docker compose` 源码，实现多容器应用的跨主机部署，运行在 **开发机** 上。
+ health_check：健康检查组件，循环遍历宿主机的容器状态信息，并且存储在分布式存储服务 `consul` 中，为之后的 **高可用** 等预留接口，作为容器运行在 **每台** 主机上。
+ log：日志收集组件，用来收集用户部署日志和应用容器打印日志，进而做进一步的分析，运行在 **每台** 主机上。


## 搭建开发集群
集群主机操作系统均为 ubuntu 14.04，要求内核版本号 ≥3.16，否则需升级内核：
```
uname -a

sudo apt update
sudo apt upgrade
```
集群中共有三台主机，此外还有一台开发机。集群的三台主机之间可以通过ssh免密码互相登录，开发机也可以ssh登陆到各集群主机。
集群中三台主机的ip和hostname分别为（写入`/etc/hosts`）：
```
192.168.0.218   nap0  mfsmaster
192.168.0.219   nap1
192.168.0.220   nap2
```
使用的用户名均为 `nap` 。其中 nap0 作为主节点。开发主机 **未** 列出。


### 安装软件和镜像
在每台主机（nap0~nap2）上分别执行以下步骤：

#### 安装docker
```
wget -qO- https://get.docker.com/ | sh

# 如果已安装了docker，使用下面的命令更新到最新版本    
sudo apt-get upgrade docker-engine

docker --version
# Docker version 1.10.3, build 20f81dd

# 把docker加到sudo权限组里面，执行docker命令不再需要加sudo，重新登陆后生效   
sudo usermod -aG docker nap
exit
```

#### 配置docker restful api（这里没有使用安全认证）
```
# 修改docker 参数
# a) 对ubuntu 14.04, 修改 /etc/default/docker
DOCKER_OPTS="
-H unix:///var/run/docker.sock    
-H tcp://0.0.0.0:2375   

# 重新启动docker daemon
sudo service docker restart

# b)对ubuntu 15.04及更高版本，及rhel/centos 7等使用systemd的系统，参考
# https://docs.docker.com/engine/articles/systemd/ 和
# https://coreos.com/os/docs/latest/customizing-docker.html
cd  /lib/systemd/system/
sudo sh -c 'cat >docker-tcp.socket' <<EOF
[Unit]
Description=Docker Socket for the API

[Socket]
ListenStream=2375
BindIPv6Only=both
Service=docker.service

[Install]
WantedBy=sockets.target
EOF

cd ~
# 重新启动docker daemon
systemctl enable docker-tcp.socket
systemctl stop docker
systemctl start docker-tcp.socket
systemctl start docker

# 测试restful api
curl localhost:2375/info | python -mjson.tool
```

#### 安装consul
```
consul_ver=0.6.3
wget https://releases.hashicorp.com/consul/${consul_ver}/consul_${consul_ver}_linux_amd64.zip
sudo apt install unzip
unzip unzip consul_0.6.3_linux_amd64.zip
sudo mv consul /usr/local/bin
rm consul_0.6.3_linux_amd64.zip
```

#### 安装moosefs-client    
```
wget -O - http://ppa.moosefs.com/moosefs.key | sudo apt-key add -    
sudo sh -c 'echo "deb http://ppa.moosefs.com/stable/apt/ubuntu/trusty trusty main" > /etc/apt/sources.list.d/moosefs.list'     
sudo apt update    
sudo apt install moosefs-client

mfsmount --version
# MFS version 2.0.88-1
# FUSE library version: 2.9.4
# fusermount version: 2.9.4
```

#### 准备 docker 镜像
```
docker pull mysql

# 按照`nap-core/moosefs/`下各目录的`Dockerfile`，依次build moosefs master, chunkserver 和 metalogger 镜像
cd ~/nap-core/moosefs/mfs_master
docker build -t mfs_master:latest .

cd ~/nap-core/moosefs/mfs_chunkserver
docker build -t mfs_chunkserver:latest .

cd ~/nap-core/moosefs/mfs_metalogger
docker build -t mfs_metalogger:latest .

Todo: 若使用了内部的docker registry，可将上面构建的镜像push到registry，然后从其它主机pull下来。
```

#### 安装python-pip
```
sudo apt install python-pip python3-pip
```

### 配置consul，overlay网络 和 moosfs

#### 配置consul集群
```
# 以nap0作为master节点
consul agent -server -ui -bootstrap-expect 1 -data-dir /tmp/consul -bind=192.168.0.218 -client=0.0.0.0 &>/dev/null &    

# 以nap1和nap2作为slave节点
# 在nap1上
consul agent -data-dir /tmp/consul -bind=192.168.0.219 -client=0.0.0.0 &>/dev/null &
consul join  --rpc-addr=192.168.0.219:8400 192.168.0.218

# 在nap2上
consul agent -data-dir /tmp/consul -bind=192.168.0.220 -client=0.0.0.0 &>/dev/null &
consul join  --rpc-addr=192.168.0.220:8400 192.168.0.218

# 验证，在集群任一主机上执行  
consul members

# 或在开发机上执行（需安装consul，但不必执行上述命令）
consul members --rpc-addr=192.168.0.218:8400

# 也可查看web ui
http://192.168.0.218:8500/ui
```

#### 在 docker daemon 参数中指定consul的位置
对集群中的每台主机，
```
# a) 对ubuntu 14.04, 修改 /etc/default/docker
# 注意，eth0 是主机ip地址 192.168.0.218/219/220 对应的网卡，是docker restful api对应ip的网卡
DOCKER_OPTS="
-H unix:///var/run/docker.sock    
-H tcp://0.0.0.0:2375
--cluster-store=consul://192.168.0.218:8500    
--cluster-advertise=eth0:2375

# 退出后重启docker daemon
sudo service docker restart

# b)对ubuntu 15.04及更高版本，及rhel/centos 7等使用systemd的系统
# 修改 /lib/systemd/system/docker.service
[Service]
ExecStart=/usr/bin/docker daemon -H fd:// --cluster-store=consul://192.168.0.218:8500 --cluster-advertise=eth0:2375

# 退出后重启docker daemon
sudo systemctl daemon-reload
sudo systemctl restart docker
```

#### 创建 overlay 网络，验证consul 键值存储配置

```  
# 在任一主机上
docker network create -d overlay test

# 在任一主机上，查看刚创建的test网络
docker network ls

# 在nap0上启动一个测试容器
docker run -ti --name t1 --net test busybox /bin/sh

# 在nap1上启动一个测试容器
docker run -ti --name t2 --net test busybox /bin/sh    

# 看看这两个测试容器彼此能否通过ip和name ping通。
```

> 注意，启动容器时指定的 --hostname（或 -h）虽然会被写入各容器的/etc/hosts，但不能被用来 ping 通。只能使用 --name 参数来指定名字。

### 部署moosefs    
```
# 在每台主机上
sudo mkdir /moosefs_data    
docker run -tid --name mfs_chunkserver --net host -v /moosefs_data/:/moosefs mfs_chunkserver bash    

# 在 nap0 上（作为mfs master）
docker run -tid --name mfs_master --net host mfs_master bash    

# 如果之前没有设置各主机的hosts，则需修改主机的 /etc/hosts，增加下面一行（因为使用的是 host 网络模式，会更新容器内的对应文件）    
192.168.0.218     mfsmaster    

# 由于moosefs相关镜像制作问题，需进入容器内手工执行命令来启动服务
# 在nap0，进入 mfs_master 容器
docker attach mfs_master
    /etc/init.d/moosefs-master start    
# 按快捷键 Ctrl + P, Q 退出容器的交互终端 (不要通过执行exit来退出容器，否则容器会停止运行)。

# 在各主机，进入 mfs_chunkserver 容器
docker attach mfs_chunkserver
    chown -R mfs:mfs /moosefs
    /etc/init.d/moosefs-chunkserver start

# 在主机 nap0 上验证mfs设置是否正确    
docker exec -ti mfs_master mfscli -SCS    

+---------------------------------------------------------------------------------------------------------------------------+
|                                                       Chunk Servers                                                       |
+---------+------+----+---------+------+-------------+-------------------------------------+--------------------------------+
|         |      |    |         |      |             |         'regular' hdd space         | 'marked for removal' hdd space |
| ip/host | port | id | version | load | maintenance +--------+---------+---------+--------+--------+------+-------+--------+
|         |      |    |         |      |             | chunks |   used  |  total  | % used | chunks | used | total | % used |
+---------+------+----+---------+------+-------------+--------+---------+---------+--------+--------+------+-------+--------+
|    nap0 | 9422 |  3 |  2.0.88 |    0 |         off |      0 | 3.5 GiB | 183 GiB |  1.93% |      0 |  0 B |   0 B |      - |
|    nap1 | 9422 |  2 |  2.0.88 |    0 |         off |      0 | 3.5 GiB | 183 GiB |  1.93% |      0 |  0 B |   0 B |      - |
|    nap2 | 9422 |  1 |  2.0.88 |    0 |         off |      0 | 3.5 GiB | 183 GiB |  1.93% |      0 |  0 B |   0 B |      - |
+---------+------+----+---------+------+-------------+--------+---------+---------+--------+--------+------+-------+--------+
```

## 在开发机上部署 nap-core

```
git clone git@github.com:icsnju/nap-core.git   
cd nap-core    
sudo python setup.py install
```

### Todo: 安装 nap-api 和 nap-desktop
