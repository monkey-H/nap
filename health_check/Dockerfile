FROM ubuntu:14.04
MAINTAINER < nap 5681713@qq.com>

RUN apt-get update && apt-get install -y python wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py 
RUN pip install python-consul docker-py
COPY update_status.py /

ENTRYPOINT ["/usr/bin/python", "/update_status.py"]
