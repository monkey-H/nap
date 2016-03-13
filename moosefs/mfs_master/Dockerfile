FROM ubuntu:14.04
MAINTAINER hmonkey <5681713@qq.com>

RUN apt-get install -y wget openssh-server
RUN wget -O - http://ppa.moosefs.com/moosefs.key | apt-key add -
RUN echo "deb http://ppa.moosefs.com/stable/apt/ubuntu/trusty trusty main" > /etc/apt/sources.list.d/moosefs.list
RUN apt-get update
RUN apt-get install -y moosefs-master moosefs-cli
RUN cp /etc/mfs/mfsmaster.cfg.dist /etc/mfs/mfsmaster.cfg
RUN cp /etc/mfs/mfsexports.cfg.dist /etc/mfs/mfsexports.cfg
RUN sed -i "s/MFSMASTER_ENABLE=false/MFSMASTER_ENABLE=true/g" "/etc/default/moosefs-master"

CMD ["/etc/init.d/moosefs-master", "start"]
