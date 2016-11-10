# restful api for nap application
> NAP的restful api是通过JSON来对平台进行管理，包括平台硬件的监控、应用的创建、状态的查询以及文件管理等。restful api是通过Django自身提供的[REST framework](http://www.django-rest-framework.org/)实现的，详见链接。

## 环境依赖：
> sudo pip install django==1.8.4    
> sudo pip install django-grappelli     
> sudo apt-get install python-ldap        
> sudo pip install djangorestframework     
> sudo pip install fs     

## 安装部署方法
测试阶段使用django自带的http server，运行方式是进入项目根目录，即manage.py所在目录，运行一下命令:
```
$ python manage.py runserver 0.0.0.0:8000
```
同样，django项目也可以使用apache服务器,只需要进行简单的设置即可，详见django官方文档[How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/)

## app_api: 应用的状态信息
该部分是对运行在NAP平台上的应用进行管理的接口，包括应用和服务的创建、应用状态的获取以及应用的开启和暂停等。

所有请求使用token进行认证，既用户进行信息的请求前，需要先认证，即下面5对应的操作，认证成功后，在进行请求时，需要将token置于Http的头部字段Authorizations中，curl和httpie对应的示例如下：
```
curl -X GET http://127.0.0.1:8000/app/porjects/ -H 'Authorizations:Token d83***3d8'

http http://127.0.0.1:8000/app/projects/ Authorizations:'Token d83***3d8'
```
这里认证的使用的数据库是LDAP数据库:     
> LDAP是一种轻量级的目录管理协议(LightWeight Directory Access Protocal)，它是以树状的层次结构来存储数据，类似于UNIX的目录树。LDAP数据库是一种对读操作进行优化的数据库，当系统的读写比例比较大时，LDAP会体现出极高的性能；此外因为LDAP的存储结构是树的形式，可以轻易的将树的一个分支迁移到其他的树中，所以它管理的数据是非常便携或易于共享的。针对用户认证管理这种改动不是很频繁的事务，一般都采用LDAP的方案。Django本身对LDAP也是支持的，只需要在配置文件中添加相关配置即可。


1. projects的请求
    - 方法: GET
    - url: /app/projects
    - 参数: {'username':xxx, 'start':xxx, 'limit':xxx}
    - 返回值:    
      参数错误时，返回400     
      token错误时，返回401 UNAUTHORIZED
      参数正确，返回Json格式数据
        ```
        {
    	    "items": [
    	        [
                    "test",
                    "git@github.com:monkey-H/rest_app.git"
    	        ],
                [
                    "test2",
                    "git@github.com:monkey-H/rest_app.git"
                ],

    	    ],
    	    "total": 2,
    	    "success": "true"
    	}
        ```

2. projects创建
    - 方法: POST
    - url: /app/projects
    - 参数: {'username':xxx, 'project':xxx, 'url':xxx}
    - 返回值:
      请求参数错误情况下返回400
      token错误时，返回401 UNAUTHORIZED
      参数正确，根据提供的参数，返回相应的信息
        ```
        {
            log: something
        }
        ```

3. project删除
    - 方法: DELETE
    - url: /app/projects/exp_poj
    - 参数: {}
    - 返回值:
      token错误时，返回401 UNAUTHORIZED
      认证成功, 返回相应的信息
        ```
        {
            Delete: success/false
            log: something
        }
        ```

4. 一个project对应的services列表
    - 方法: GET
    - url: /app/projects/exp_poj
    - 参数: {}
    - 返回值:   
      请求错误情况下返回400
      token认证错误返回401 UNAUTHORIZED
      正确时，返回请求的实例，如下:   
        ```
        {
    	    "items": [
    	        {
    	            "ip": "114.212.189.140",
    	            "name": "testmpi_1_master",
                    "port": XX,
                    "status": XX,
    	        },
    	        {
    	            "ip": "114.212.189.136",
    	            "name": "testmpi_1_slaves@1",
                    "port": XX,
                    "status": XX,
    	        }
    	    ],
            "total": 2,
            "success": "true",
    	}
        ```


4. 用户认证使用的是rest-framework自带的TokenAuthentication.
    - 方法: Post
    - url: /auth
    - 参数: {'username':xxx, 'password':xxx}
    - 返回值:
      请求正确，并成功认证返回    
        ```
        {
            token: *******
        }
        ```
      请求错误时,认证失败时会返回400,并给出相应的提示信息。   
    使用httpie进行请求示例：
    ```
    http --form post http://127.0.0.1:8000/app/auth username="***" password="***"
    ```


## filebrowser:访问主机文件系统
该部分是从开源项目[django-extjs-filebrowser](https://github.com/revolunet/django-extjs-filebrowser)的后台Django部分直接迁移出来的，针对django-restframework框架进行了相应的修改。

1. 请求一个文件夹下的目录树  
    - 方法: POST  
    - url: /fs/filebrowser/api/  
    - 参数: {'cmd': "get", 'path': "key/path"}
     (key 为配置文件中主机提供的文件系统的根目录,目前只有localfolder可选,path为请求的路径)   
    - 返回值: json格式数据，示例如下:   
    ```
    $ http --form POST http://114.212.86.206:8000/fs/filebrowser/api/ cmd="get" path="localfolder/new/"
    (请求localfolder对应的根目录下new的目录树)
    [
        {
            "created_time": "2015-10-27T13:43:31.150469",
            "iconCls": "icon-file-txt",
            "items": [],
            "leaf": true,
            "modified_time": "2015-10-27T13:43:31.110469",
            "size": 12,
            "text": "hello6.txt"
        },
        {
            "created_time": "2015-11-09T09:11:14.739974",
            "iconCls": "icon-file-jpg",
            "items": [],
            "leaf": true,
            "modified_time": "2015-10-27T14:02:38.394490",
            "size": 925306,
            "text": "test.jpg"
        }
    ]
    ```

2. 新建目录
    - 方法: POST  
  	- url: fs/filebrowser/api/   
  	- 参数: {'cmd': "newdir", 'path': "key/path"}
  	- 返回值:  
    参数正确时,返回数据
    ```
    {'success':True}
    ```
    否则根据情况返回400,404  

3. 重命名
  	- 方法: POST  
  	- url: fs/filebrowser/api/  
  	- 参数: {'cmd': "rename", 'oldname': "key/path", 'newname': "key/path"}
  	- 返回值:  
    参数正确时,返回{'success': True},错误时返回400    

4. 删除文件或文件夹  
    - 方法: POST  
    - url: fs/filebrowser/api/  
  	- 参数: {'cmd': "delete",'path': "key/path"}
  	- 返回值:  
    参数正确时,返回{'success': True},错误时返回404  

5. 查看文件:
  	- 方法: GET  
    - url: fs/filebrowser/api/  
  	- 参数: {'cmd': "view", 'file': "key/path"}
  	- 返回值:  
    参数正确时,返回文件的内容,错误时返回404  

6. 下载文件:
  	- 方法: GET  
  	- url: fs/filebrowser/api/  
  	- 参数: {'cmd': "download", 'file': "key/path"}
  	- 返回值:   
    参数正确时,下载文件,错误时返回404   

7. 上传文件:  
	- 方法: POST
	- url: /fs/upload/
	- 参数, 请求方式有两种:
	   * XMLHttpRequest:  
		```
		xhr = new XMLHttpRequest()
		xhr.open('POST', 'http://127.0.0.1:8000/fs/filebrowser/upload/', true);
		xhr.setRequestHeader("X-File-Name","localfolder/new/" + file.name);
		xhr.setRequestHeader("X-Requested-With","XMLHttpRequest");
		xhr.send(file);   
		```
	   * 一般post请求  
		```
		formdata = new FormData()
		formdata.append("path","localfolder/new");
		formdata.append("file1",file);
		xhr.open('POST', 'http://127.0.0.1:8000/fs/filebrowser/upload/', true);
		xhr.send(formdata);
		```
	- 返回值:   
	参数等正确时，返回  
	```
	{
        "success":True,
        files:{}
    }
	```
	请求错误时，返回400或404异常
