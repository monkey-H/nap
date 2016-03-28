# 健康检查组件

运行在每个主机的容器中，检测主机上的所有容器的运行状态，并存储到consul kv里面。
相当于`docker ps -a`命令
每个容器对应的key为 
使用host网络，这样容器中可以直接使用localhost（127.0.0.1:2376）来访问docker engine

监控：
利用google提供的cadvisor，抠图，抠出我们希望留下的图，然后，做成我们要的监控。
cadvisor是通过conatiner_id来进行查找对应的容器的状态，我们要有对应的函数，返回相应的container id.


        # todo 容器命名约定，保证容器名不发生冲突，易解析。建议用 . 做分隔符。格式为svc-num.prj.user
        # 如果在yml中指定了containername，则用该值，否则为svc name
        # 用户的容器名不能使用-，因为用来分割用户名，项目名，svc名
