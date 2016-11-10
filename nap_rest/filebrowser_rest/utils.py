# coding: utf-8
from settings import sources
import os
import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response


def download(py_fs, path, attachment=False):
    '''
    下载或查看文件
    '''
    if py_fs.isdir(path):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if not py_fs.exists(path):
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    file = py_fs.open(path, 'rb')
    import mimetypes
    inFileName = path.split('/')[-1]
    mt = mimetypes.guess_type(inFileName)
    response = HttpResponse(content_type=mt)
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % inFileName
    response.write(file.read())
    return response


def dirToJson(inFs, path='/', recursive=False):
    '''
    将一个指定文件夹目录树返回,json格式数据
    '''
    data = []
    if not inFs.exists(path) or not inFs.isdir(path):
        return data
    for item in inFs.listdir(path=path):
        fPath = os.path.join(path, item)
        infos = inFs.getinfo(fPath)
        isLeaf = not inFs.isdir(fPath)
        iconCls = not isLeaf and 'icon-folder' or 'icon-file-%s' % item[item.rfind('.') + 1:]
        row = {
            'text': item
            , 'size': infos.get('size', 0)
            , 'modified_time': infos.get('modified_time', datetime.datetime.now()).isoformat()
            , 'created_time': infos.get('created_time', datetime.datetime.now()).isoformat()
            , 'leaf': isLeaf
            , 'filetype': iconCls
            , 'items': []
            , 'path': 'localfolder/' + fPath
        }
        # recursive and isdir ?
        if not isLeaf and recursive:
            row['items'] = dirToJson(inFs, path=fPath, recursive=recursive)

        data.append(row)
    return data


def splitPath(inPath):
    '''
    将参数传递的数据进行分割，path格式为 "key/subpath",其中key对应的是字典sources的key,
    value包括文件系统类型以及对应类型的pyfilesystem的参数,详见settings.py
    '''
    if not inPath:
        return None, None
    if inPath[0] == '/':
        inPath = inPath[1:]
    root = inPath.split('/')[0]
    path = '/'.join(inPath.split('/')[1:])
    return root, path


def getFsFromKey(key, username):
    if key in sources.keys():
        source = sources[key]
        root_path = source['params']['root_path'] + username
        cur_fs = source['cls'](root_path)
        return cur_fs
    else:
        return None
