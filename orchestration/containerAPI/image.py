import time
from docker import Client


def format_size(size):
    if size < 1000:
        return size
    elif size < 1000000:
        return str('%.2f' % (size / 1000)) + 'k'
    elif size < 1000000000:
        return str('%.2f' % (size / 1000000)) + 'm'
    elif size < 1000000000000:
        return str('%.2f' % (size / 1000000000)) + 'g'


class Image(object):
    """
    image class for docker
    """

    def __init__(self, client, name):
        self.name = name
        self.cli = client

        info = self.get_info(name)

        self.tag = info['tag']
        self.size = info['size']
        self.create_time = info['create_time']

    def get_info(self, name):
        dic = self.cli.inspect_image(name)

        info = {'tag': dic['RepoTags'], 'size': format_size(float(dic['VirtualSize']))}

        time_num = time.mktime(time.strptime(dic['Created'].split('.')[0], '%Y-%m-%dT%H:%M:%S'))
        create_time = time.localtime(time_num)
        format_time = time.strftime('%Y-%m-%d %H:%M:%S', create_time)
        info['create_time'] = format_time

        return info

    @classmethod
    def get_list(cls, url, version):
        cli = Client(base_url=url, version=version)

        image_list = cli.images(all=True)
        rel = []

        for image in image_list:
            item = {}

            name_tag = image['RepoTags'][0]

            name = name_tag.split(':')[0]
            if name == '<none>':
                continue

            item['name'] = name
            item['tag'] = name_tag.split(':')[1]

            create_time = time.localtime(image['Created'])
            format_time = time.strftime('%Y-%m-%d %H:%M:%S', create_time)

            item['create_time'] = format_time
            item['size'] = format_size(float(image['VirtualSize']))

            rel.append(item)

    @classmethod
    def destroy_image(cls, url, version, name):
        cli = Client(base_url=url, version=version)

        cli.remove_image(image=name)

        return rel
