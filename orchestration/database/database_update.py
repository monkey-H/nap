from docker import Client
import MySQLdb
from orchestration import config

# database_url = '114.212.189.147'
# c_version = '1.21'
# split_mark = '-'
# client_list = ['114.212.189.147:2376', '114.212.189.140:2376']

def tuple_in_tuple(db_tuple):
    ret_data = []
    for item in db_tuple:
        ret_data.append(item[0])
    return ret_data

def get_net(username, password):
     db = MySQLdb.connect(config.database_url, username, password, username)
     cursor = db.cursor()
     cursor.execute("select net from info where name='%s'" % username)
     data = cursor.fetchone()
     db.close()
     return data[0]

def set_net(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into info(net) values(%s) where name='%s'" % (username, username))
    db.commit()
    db.close()

def get_volume(username, password):
     db = MySQLdb.connect(config.database_url, username, password, username)
     cursor = db.cursor()
     cursor.execute("select volume from info where name='%s'" % username)
     data = cursor.fetchone()
     db.close()
     return data

def set_volume(self, username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into info(volume) values(%s) where name='%s'" % (username, username))
    db.commit()
    db.close()

def service_list(username, password, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select name from service where project = '%s'" % project_name)
    data = cursor.fetchall()
    db.close()

    return tuple_in_tuple(data) if data else None

def create_service(username, password, service_name, service_id, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into service values('%s', %d, '%s')" % (service_name, service_id, project_name))
    db.commit()
    db.close()

def delete_service(username, password, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("delete from service where project = '%s'" % project_name)
    db.commit()
    db.close()

def project_exists(username, password, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select name from project where name='%s'" % project_name)
    data = cursor.fetchone()
    db.close()

    return True if data else False

def roll_back(username, password, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()

    logs = ''
    srv_list = service_list(username, password, project_name)
    if srv_list:
        for service_name in srv_list:
            url = machine_ip(username, password, project_name, service_name)
            if url == '-':
                continue
            cli = Client(base_url=url, version=config.c_version)
            full_name = username + config.split_mark + project_name + config.split_mark + service_name
            if container_exists(cli, full_name):
                logs = logs + full_name + '\n' + cli.logs(container=full_name) + '\n'
                cli.stop(container=full_name)
                cli.remove_container(container=full_name)
        cursor.execute("delete from service where project='%s'" % project_name)
        cursor.execute("delete from project where name='%s'" % project_name)
        db.commit()
        db.close()

    return logs

def container_exists(cli, container_name):
    containers = cli.containers(all=True)
    for k in containers:
        if '/' + container_name in k['Names']:
            return True
    return False

def machine_ip(username, password, project_name, service_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select machine from service where name = '%s' and project = '%s'" % (service_name, project_name))
    data = cursor.fetchone()
    print project_name
    print service_name
    print data
    if data == None:
        db.close()
        return '-'
    else:
        cursor.execute("select ip from machine where id = %s" % data[0])
        data = cursor.fetchone()
        db.close()
        return data[0]

def get_machine(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select ip from machine")
    data = cursor.fetchall()
    db.close()
    return tuple_in_tuple(data)

def create_project(username, password, project_name, url):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into project(name, url) values('%s', '%s')" % (project_name, url))
    db.commit()
    db.close()

def delete_project(username, password, project_name):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("delete from project where name ='%s'" % project_name)
    db.commit()
    db.close()

def database_exist(username, password):
    db = MySQLdb.connect(config.database_url, config.rootname, config.rootpass)
    cursor = db.cursor()
    cursor.execute("show databases;")
    database_list = cursor.fetchall()
    database_l = tuple_in_tuple(database_list)

    for user in database_l:
        if user == username:
            return True

    return False

def create_basetable(username, password):
    db = MySQLdb.connect(config.database_url, config.rootname, config.rootpass)
    cursor = db.cursor()
    cursor.execute("create database %s;" % username)
    cursor.execute("create user '%s'@'%s' identified by '%s';" % (username, '%', password))
    cursor.execute("grant all on %s.* to '%s'@'%s';" % (username, username, '%'))
    db.commit()
    db.close()

    # create some tables for this user
    user_db = MySQLdb.connect(config.database_url, username, password, username)
    user_cursor = user_db.cursor()
    user_cursor.execute("create table info(name char(50) not null, net char(50), volume char(50));")
    user_cursor.execute("create table machine(id int unsigned not null, ip char(50));")
    user_cursor.execute(
        "create table project(id int unsigned not null auto_increment primary key, name char(50), url char(50));")
    user_cursor.execute("create table service(name char(50), machine int unsigned, project char(50));")
    user_cursor.execute("insert into info values('%s', '%s', '%s_volume');" % (username, username, username))
    client_id = 0
    for client in config.client_list:
        user_cursor.execute("insert into machine values(%d, '%s');" % (client_id, client))
        client_id += 1
    # user_cursor.execute("insert into machine values(0, '192.168.56.105:2376');")
    # user_cursor.execute("insert into machine values(1, '192.168.56.106:2376');")
    user_db.commit()
    user_db.close()

def create_user(username, password):
    if database_exist(username, password):
        return False, "username: %s already exists, please try anoter name"

    create_basetable(username, password)
    return True, "insert into mysql"

def delete_user(username):
    db = MySQLdb.connect(config.database_url, config.rootname, config.rootpass)
    cursor = db.cursor()
    cursor.execute('drop user %s' % username)
    cursor.execute('drop database %s' % username)
    cursor.execute('flush privileges')
    db.commit()
    db.close()

def project_list(username, password, begin, length):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select name, url from project limit %s,%s" % (begin, length))
    data = cursor.fetchall()
    db.close()
    return data
