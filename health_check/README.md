

heart_beat作为健康检查组件，机器中所有的机器都应该有。
需要在集群中每个节点上build此镜像，然后，运行。注意，运行的时候，参数是ｈｏｓｔ节点的ｉｐ。
heart_beat组件是检测主机上的存在的容器的运行状态，并收集，存储到consul kv里面。

监控：
利用google提供的cadvisor，抠图，抠出我们希望留下的图，然后，做成我们要的监控。

cadvisor是通过conatiner_id来进行查找对应的容器的状态，我们要有对应的函数，返回相应的container id.

