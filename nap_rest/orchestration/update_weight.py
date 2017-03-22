from docker import Client
import requests
import time

from orchestration.container_api import client
from orchestration.nap_api import app_info
from orchestration import config

def get_container_load(username, project_name, service_name, container_name):
    usage = app_info.container_resource_usage(username, project_name, service_name, container_name)

    if usage is None:
        return

    cpu_usage = usage["cpu_usage"]
    mem_usage = usage["mem_usage"]

    cpu_weight = int((1-cpu_usage)*10)
    mem_weight = int((1-mem_usage)*10)

    weight = cpu_weight
    if (cpu_weight > mem_weight):
        weight = mem_weight

    return weight


def get_container_weight():

    urls = []
    usages = []
    names = []
    weight = []
    names.append('114.212.189.147:32777')
    names.append('114.212.189.147:32778')
    names.append('114.212.189.147:32779')
    names.append('114.212.189.147:32780')
    names.append('114.212.189.147:32781')
    names.append('114.212.189.147:32782')
    names.append('114.212.189.147:32783')
    names.append('114.212.189.147:32784')
    names.append('114.212.189.147:32785')
    names.append('114.212.189.147:32786')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/b2a056edb4efa10d1f8a10d7cf23e60290e1221e7a4298792698d0d001044a76')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/89b1d03e3131497471a369d02638665aa7f572702b1368663912214a533a1673')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/e6064ea88ee1804c95a3e083dd00bb686779e1fc49b2a428503980918de2855b')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/935cce1850b6f8490181a28613b484735fe02426a41e187e4602a51f0b790657')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/921f21aefb99e70ae7d31073c6f111534c7144d4c49c010cd13da715288a3504')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/af58f0cb938b8068d5c0f8d3d90443769eefd307de4356793e7e39a36cf35e29')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/004a9055e88e607c0a5c645b6ca4642b6553f588f01cc40f189949f42325fa16')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/8508a675576a68472ef255d49c690b33cca12a0f8587b3466ccc974aec64425c')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/139998732aa8f7433b8714347e31d108c59cb03f9a211603cd1c6fc3ba2e4f41')
    urls.append('http://114.212.189.147:8080/api/v1.2/docker/62fe0910712e810d6550815e4d39da1fe9cf47f486835c0bbca8bd2c0187b03a')

    for url in urls:
        response = requests.get(url)

        if response.status_code == 500:
            return None

        true = True
        false = False

        di = eval(response.text)
        rel = []

        for item in di:
            for node in di[item]['stats']:
                dic = {'mem_usage': node['memory']['usage'],
                       'mem_total': di[item]['spec']['memory']['limit'],
                       'cpu_usage': node['cpu']['usage']['total'],
                       'cpu_total': di[item]['spec']['cpu']['limit'],
                       'timestamp': node['timestamp']}

                rel.append(dic)

        re = []

        for index in range(len(rel)):
            if not index == 0:
                pre = rel[index - 1]
                cur = rel[index]

                gap = time_gap(pre['timestamp'], cur['timestamp'])

                dic = {'timestamp': cur['timestamp'],
                       # 'file_usage': float(cur['file_usage'])/float(cur['file_total']),
                       # 'memory_usage': float(cur['memory_usage'])float(cur['memory_total']),
                       'mem_usage': float(cur['mem_usage']),
                       'cpu_usage': (float(cur['cpu_usage']) - float(pre['cpu_usage'])) / gap}

            re.append(dic)

        usages.append({"cpu_usage": re[-1]["cpu_usage"]})

    for item in usages:
        weight.append((int)((1-item["cpu_usage"])*5))

    for index,item in enumerate(names):
        cli = client.Client('114.212.189.140:2376', config.c_version).client
        tt = cli.exec_create(container='nginx',
                             cmd='/bin/bash -c \"cd /etc/nginx/conf.d && sh replace_weight.sh %s %s && /etc/init.d/nginx reload\"' % (
                                 item, weight[index]))
        cli.exec_start(exec_id=tt, detach=True)


def time_gap(pre, cur):
    pre_after = float(pre.split(".")[1][:-1])
    cur_after = float(cur.split(".")[1][:-1])

    pre_before = pre.split(".")[0]
    cur_before = cur.split(".")[0]

    pre_time = time.mktime(time.strptime(pre_before, '%Y-%m-%dT%H:%M:%S'))
    cur_time = time.mktime(time.strptime(cur_before, '%Y-%m-%dT%H:%M:%S'))

    gap = (cur_time - pre_time) * 1000000000 + cur_after - pre_after

    return gap


if __name__ == "__main__":
    while True:
        print "one circle"
        time.sleep(5)
        get_container_weight()
