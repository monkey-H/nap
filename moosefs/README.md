# moosefs分布式存储组件，用来整合存储资源。

其中`master`容器和`metalogger`容器建议运行在不同的主机上。
`chunkserver`是提供数据块的组件，可以与`master`运行在同一主机上。为降低负载，也可为`master`分配单独的主机。

受 docker volume 不支持直接将nfs/mfs目录挂载为data volume的限制，`client`需运行在主机上，而不能运行在容器中。

如果使用私有的docker registry可以将各镜像build完成后push到该registry。
否则可在集群中的每台机器上build　chunkserver镜像，在master主机上build master容器，另一台机器上build metalogger镜像，然后分别运行。

注意，启动moosefs容器需要使用 `--net host`参数，即使用主机的网络，因为我们在主机上运行client来挂载mfs，需要在所有的主机上均可访问容器的网络。
```
docker run -d --name chunkserver --net host -v /moosefs_data/:/moosefs mfs_chunkserver bash
docker run -d --name mfs_master  --net host                            mfs_master      bash
```
注意，启动后，需确认各容器内的`/etc/hosts`文件，是否存在 mfsmaster 的ip，该ip是运行mfs_master容器的那台主机的ip。
