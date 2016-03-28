# MySQL数据库组件

直接使用MySQL的一个容器。
我们希望可以使用我们的平台来部署自己的组件，所以，用docker-compose.yml文件来描述。

该容器使用的桥接（NAT）网络，并映射到主机端口，数据库ip即为所在主机的ip。

数据库的表定义等初始化代码在`orchestration/database`
