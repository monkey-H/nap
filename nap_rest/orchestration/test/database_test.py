from orchestration.database import database_update
# import MySQLdb
# from orchestration import config

config = {'name': 'hello', 'scale': 2}
# if __name__ == '__main__':
    # ip_list = ['114.212.189.147:2376', '114.212.189.140:2376']
    # database_update.create_machine(ip_list)
    # database_update.create_user('test', 'test@email.com')
    # database_update.create_project()
database_update.create_project('test', 'project', 'project@github.com')
    # print database_update.get_machine()
print database_update.project_list('test', 0, 2)
print database_update.project_exists('test', 'project')
print database_update.project_exists('test', 'projects')
database_update.create_service('test', 'project', 'service', config, 2)
print database_update.service_list('test', 'project')
database_update.create_container('test', 'project', 'service', 'service0', '114.212.189.147:2376')
print database_update.container_list('test', 'project', 'service')
print database_update.container_ip('test', 'project', 'service', 'service0')
# print database_update.delete_container_by_name('test', 'project', 'service', 'service0')
print database_update.container_list('test', 'project', 'service')
    # print database_update.service_list('test', 'project')
    # print database_update.project_list('test', 0, 2)
# database_update.delete_project('test', 'project')
print database_update.project_list('test', 0, 10)

# db = MySQLdb.connect(config.database_url, config.database_user, config.database_passwd, config.database)
# cursor = db.cursor()
# cursor.execute("select name from user")
#
# data = cursor.fetchall()
# for item in data:
#     print item[0]
#
# data = cursor.fetchall()
