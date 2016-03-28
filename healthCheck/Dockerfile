FROM python:2-alpine
MAINTAINER < nap 5681713@qq.com>
# ref: https://hub.docker.com/_/python/
# 请将该image tag设置为health-check

# requirments
RUN pip install python-consul docker-py
COPY healthCheck.py /

ENTRYPOINT ["/usr/local/bin/python", "/healthCheck.py"]
