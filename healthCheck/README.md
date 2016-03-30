# 健康检查组件

运行在每个主机的容器中，检测主机上的所有容器当前的运行状态，定时刷新到consul kv里面。
相当于`docker ps -a`命令
每个容器对应的key为 "user_name/project_name/service_name"

使用host网络，这样容器中可以直接使用localhost（127.0.0.1:2376）来访问docker engine

## todo
参考或直接采用用google的[cAdvisor](https://github.com/google/cadvisor)。
cAdvisor即提供host的，也有关于容器的监控项，有web ui及restful api


关于容器命名约定，应保证容器名不发生冲突，易解析。建议用`. `做分隔符，格式为 svc-num.prj.user
如果在yml中指定了 container_name，则用该值，否则为 svc_name + 编号
需对用户提供的 container_name， svc_name 等做有效性检查
