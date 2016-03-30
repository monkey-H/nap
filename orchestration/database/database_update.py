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


# not use temporarily
def get_net(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select net from info where name='%s'" % username)
    data = cursor.fetchone()
    db.close()
    return data[0]


# not use temporarily
def set_net(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into info(net) values('%s') where name='%s'" % (username, username))
    db.commit()
    db.close()


# not use temporarily
def get_volume(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("select volume from info where name='%s'" % username)
    data = cursor.fetchone()
    db.close()
    return data


# not use temporarily
def set_volume(username, password):
    db = MySQLdb.connect(config.database_url, username, password, username)
    cursor = db.cursor()
    cursor.execute("insert into info(volume) values('%s') where name='%s'" % (username, username))
    db.commit()
    db.close()


def database_get(clause):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute(clause)
    data = cursor.fetchall()
    db.close()

    return data


def database_set(clause):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute(clause)
    db.commit()
    db.close()


def service_list(username, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from projects where name = '%s' and userID=(select id from user where name='%s')"
                   % (project_name, username))
    data = cursor.fetchall()

    if len(data) == 0:
        return None

    cursor.execute("select name from services where projectID='%d'" % data[0])
    data = cursor.fetchall()
    return data
    # clause = "select name from services " \
    #          "where projectID in " \
    #          "(select id from projects where name='%s' and userID in (select id from user where name = '%s')))" \
    #          % (project_name, username)
    #
    # data = database_get(clause)


def create_service(username, service_name, machine_ip, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from projects where name='%s' and userID in (select id from user where name = '%s')"
                   % (project_name, username))
    data = cursor.fetchone()
    cursor.execute("insert into services(name, projectID, IP) values('%s', %d, '%s')"
                   % (service_name, data[0], machine_ip))
    db.commit()
    db.close()


def delete_service(username, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from projects where name='%s' and userID = (select id from user where name = '%s')"
                   % (project_name, username))
    data = cursor.fetchall()
    cursor.execute("delete from services where projectID = '%s'" % data[0])
    db.commit()
    db.close()


def project_exists(username, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select * from projects where name='%s' and userID = (select id from user where name = '%s')"
                   % (project_name, username))
    data = cursor.fetchall()
    db.close()

    return True if data else False


def roll_back(username, password, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()

    logs = ''
    srv_list = service_list(username, password, project_name)
    if srv_list:
        for service_name in srv_list:
            url = service_ip(username, project_name, service_name)
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


def service_ip(username, project_name, service_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from projects where name='%s' and userID=(select id from user where name='%s')"
                   % (project_name, username))
    data = cursor.fetchone()
    print service_name
    cursor.execute("select IP from services where name='%s' and projectID='%d'" % (service_name, data[0]))
    data = cursor.fetchone()
    return data[0]


def get_machines():
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select ip from machine")
    data = cursor.fetchall()
    db.close()
    return tuple_in_tuple(data)


def get_machine(index):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select ip from machine limit %d,1" % index)
    data = cursor.fetchone()
    db.close()
    return data[0]


def create_project(username, project_name, url):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from user where name='%s'" % username)
    data = cursor.fetchone()
    print data[0]
    cursor.execute("insert into projects(name, userID, url) values('%s', '%d', '%s')" % (project_name, data[0], url))
    db.commit()
    db.close()


def delete_project(username, project_name):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from user where name='%s'" % username)
    data = cursor.fetchone()
    if len(data) == 0:
        return
    cursor.execute("delete from projects where name ='%s' and userID='%d'" % (project_name, data[0]))
    db.commit()
    db.close()


# not use again, all users use one database
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


# not use again, all users use one database
def create_basetable(username, password):
    db = MySQLdb.connect(config.database_url, config.rootname, config.rootpass)
    cursor = db.cursor()
    cursor.execute("create database '%s';" % username)
    cursor.execute("create user '%s'@'%s' identified by '%s';" % (username, '%', password))
    cursor.execute("grant all on '%s'.* to '%s'@'%s';" % (username, username, '%'))
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


def create_user(username, email):
    # if database_exist(username, password):
    #     return False, "username: %s already exists, please try anoter name"
    #
    # create_basetable(username, password)
    # return True, "insert into mysql"
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("insert into user(name, email) values('%s', '%s')" % (username, email))
    db.commit()
    db.close()


def create_machine(ip_list):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    for ip in ip_list:
        cursor.execute("insert into machine(ip) values('%s')" % ip)
    db.commit()
    db.close()


def delete_user(username):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from user where name='%s'" % username)
    data = cursor.fetchone()

    cursor.execute("delete from services where projectID in (select id from projects where userID='%d')" % data[0])
    cursor.execute("delete from projects where userID='%d'" % data[0])
    cursor.execute("delete from user where name='%s'" % username)
    db.commit()
    db.close()


def project_list(username, begin, length):
    db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
    cursor = db.cursor()
    cursor.execute("select id from user where name='%s'" % username)
    data = cursor.fetchone()
    if len(data) == 0:
        return None
    cursor.execute("select name, url from projects where userID = '%d' limit %d,%d" % (data[0], begin, length))
    data = cursor.fetchall()
    db.close()
    return data
