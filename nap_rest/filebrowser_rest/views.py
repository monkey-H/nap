# coding: utf-8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)

from filebrowser_rest.utils import (
    download,
    dirToJson,
    splitPath,
    getFsFromKey,
)


# Create your views here.
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def file_operate(request, format=None):
    username = str(request.user)
    if request.method == 'GET':
        root, path = splitPath(request.GET['path'])
    else:
        root, path = splitPath(request.data['path'])

    if root:
        cur_fs = getFsFromKey(root, username)
        if not cur_fs:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':  # 请求文件，查看或下载
        cmd = request.GET['cmd']
        if cmd not in ['view', 'download']:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        attachment = True if cmd == 'download' else False
        return download(cur_fs, path, attachment)

    elif request.method == 'POST':  # 修改或上传文件
        try:
            content = request.data['content']
            cmd = request.data['cmd']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        f_exists = 1 if cur_fs.exists(path) else 0
        if cmd == 'update':
            if not f_exists:
                return Response({'log': '{0} not exists'.format(path)}, status=status.HTTP_404_NOT_FOUND)
        else:
            if f_exists:
                return Response({'log': '{0} already exists'.format(path)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            f = cur_fs.open(path, 'wb')
            f.write(content)
            f.close()
            if cmd == 'update':
                return Response({'log': '{0} updated successfully!!'.format(path)})
            else:
                return Response({'log': '{0} created successfully!!'.format(path)})
        except:
            if cmd == 'update':
                return Response({'log': '{0} updated failed!!'.format(path)})
            else:
                return Response({'log': '{0} created failed!!'.format(path)})

    elif request.method == 'PUT':  # 修改文件名字
        root2, path2 = splitPath(request.data['newname'])
        if root != root2 or not root2:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        cur_fs = getFsFromKey(root, username)

        if not cur_fs.exists(path):
            return Response({'log': 'no such file'}, status=status.HTTP_404_NOT_FOUND)
        try:
            cur_fs.rename(path, path2)
            return Response({'rename': 'success', 'path': path2})
        except:
            return Response({'rename': 'failed', 'log': 'failed to rename file {0}'.format(path)})

    elif request.method == 'DELETE':  # 删除一个文件
        if not cur_fs.exists(path):
            return Response({'log': 'no such file'}, status=status.HTTP_404_NOT_FOUND)
        try:
            cur_fs.remove(path)
            return Response({'delete': 'suceess', 'file': path})
        except:
            return Response({'delete': 'failed', 'log': 'failed to delete file {0}'.format(path)})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def dir_operate(request, format=None):
    username = str(request.user)
    if request.method == 'GET':
        root, path = splitPath(request.GET['path'])
    else:
        root, path = splitPath(request.data['path'])

    if root:
        cur_fs = getFsFromKey(root, username)
        if not cur_fs:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if not cur_fs.exists(path):
            return Response([], status=status.HTTP_404_NOT_FOUND)
        data = dirToJson(cur_fs, path, recursive=False)
        return Response(data)

    if request.method == 'POST':
        if cur_fs.exists(path):
            return Response({'newdir': 'fail', 'log': 'directory already exists!!'})
        cur_fs.makedir(path, recursive=True)
        return Response({'newdir': 'success', 'directory': 'path'})

    if request.method == 'DELETE':
        if not cur_fs.exists(path):
            return Response({'delete': 'fail', 'log': 'no such directory'}, status=status.HTTP_400_BAD_REQUEST)
        if cur_fs.isdir(path):
            cur_fs.removedir(path, force=True)
        else:
            cur_fs.remove(path)
        return Response({'delete': 'success', 'directory': path})

    if request.method == 'PUT':
        root2, path2 = splitPath(request.data['newname'])
        if not root2 or not root == root2:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if not cur_fs.exists(path):
            return Response({'log': 'desc does not exists'}, status=status.HTTP_404_NOT_FOUND)
        try:
            cur_fs.rename(path, path2)
            return Response({'rename': 'success'})
        except:
            return Response({'log': 'something wrong in renaming directory'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def cpmv(request):
    '''
    复制或者移动文件或文件夹
    '''
    username = str(request.user)
    if request.method == 'PUT':
        '''cmd指定复制或移动，src为要移动的文件或文件夹，dst为指定的目录'''
        try:
            cmd = request.data['cmd']
            src = request.data['src']
            dst = request.data['dst']
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        src_root, src_path = splitPath(src)
        dst_root, dst_path = splitPath(dst)

        if src_root != dst_root:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        cur_fs = getFsFromKey(src_root, username)

        if not cur_fs.exists(src_path):
            return Response({'log': 'src does not exists'}, status=status.HTTP_404_NOT_FOUND)

        name = src_path.strip().split('/')[-1]
        if cmd == 'copy':
            try:
                if cur_fs.isdir(src_path):
                    cur_fs.copydir(src_path, dst_path + '/' + name)
                else:
                    cur_fs.copy(src_path, dst_path + '/' + name)
                return Response({'log': 'copy success...'})
            except:
                return Response({'log': 'copy failed...already exists!!!'})
        elif cmd == 'move':
            try:
                if cur_fs.isdir(src_path):
                    cur_fs.movedir(src_path, dst_path + '/' + name)
                else:
                    cur_fs.move(src_path, dst_path + '/' + name)
                return Response({'log': 'move success...'})
            except:
                return Response({'log': 'move failed...already exists!!!'})
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


def upload(request, username):
    file_list = []

    # 设置文件类型限制
    # allowed_extensions = 'jpg,jpeg,gif,png,pdf,swf,doc,docx,xls,\
    # log,xlsx,ppt,pptx,txt,c,py,cpp,go,class,java'.split(',')

    # 使用xmlhttpRequest进行请求
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        path = request.META.get('HTTP_X_FILE_NAME')
        if not path:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        root, path = splitPath(path.decode('UTF-8'))
        cur_fs = getFsFromKey(root, username)
        if not cur_fs:
            raise Response({}, status=status.HTTP_404_NOT_FOUND)

        data = request.body
        '''
        fName = path
        if not fName[fName.rfind('.')+1:].lower() in allowed_extensions:
            print 'FORBIDDEN FILE : %s ' % fName
            raise Exception('extension not allowed %s' % fName)
        '''
        f = cur_fs.open(path, 'wb')
        f.write(data)
        f.close()
        file_list.append(path)

    # 使用一般的post请求
    else:
        root, path = splitPath(request.POST['path'].decode('UTF-8'))
        cur_fs = getFsFromKey(root, username)
        if not cur_fs:
            raise Response({}, status=status.HTTP_404_NOT_FOUND)

        for key in request.FILES.keys():
            upload = request.FILES[key]
            fName = upload.name
            '''
            if not fName[fName.rfind('.')+1:].lower() in allowed_extensions:
                # todo : log + mail
                print 'FORBIDDEN FILE : %s ' % fName.encode('UTF-8')
                raise Exception('extension not allowed %s' % fName.encode('UTF-8'))
            '''
            f = cur_fs.open(path + '/' + fName, 'wb')
            for chunk in upload.chunks():
                f.write(chunk)
            f.close()
            file_list.append(fName)

    return Response({'success': True, 'file': file_list})
