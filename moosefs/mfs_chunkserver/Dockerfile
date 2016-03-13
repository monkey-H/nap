FROM ubuntu:14.04
MAINTAINER hmonkey <5681713@qq.com>

RUN apt-get install -y wget openssh-server
RUN wget -O - http://ppa.moosefs.com/moosefs.key | apt-key add -
RUN echo "deb http://ppa.moosefs.com/stable/apt/ubuntu/trusty trusty main" > /etc/apt/sources.list.d/moosefs.list
RUN apt-get update
RUN apt-get install -y moosefs-chunkserver
RUN cp /etc/mfs/mfschunkserver.cfg.dist /etc/mfs/mfschunkserver.cfg
RUN cp /etc/mfs/mfshdd.cfg.dist /etc/mfs/mfshdd.cfg
RUN mkdir /moosefs && echo "/moosefs" >> /etc/mfs/mfshdd.cfg
RUN chown -R mfs:mfs /moosefs
RUN sed -i "s/MFSCHUNKSERVER_ENABLE=false/MFSCHUNKSERVER_ENABLE=true/g" "/etc/default/moosefs-chunkserver"

CMD ["/etc/init.d/moosefs-chunkserver", "start"]
