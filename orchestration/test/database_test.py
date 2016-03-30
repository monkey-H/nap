from orchestration.database import database_update

if __name__ == '__main__':
    ip_list = ['114.212.189.147:2376', '114.212.189.140:2376']
    # database_update.create_machine(ip_list)
    # database_update.create_user('test', 'test@email.com')
    # database_update.create_project()
    # database_update.create_project('test', 'project', 'project@github.com')
    # print database_update.get_machine()
    # print database_update.project_list('test', 0, 2)
    # print database_update.project_exists('test', 'project')
    # print database_update.project_exists('test', 'projects')
    # database_update.create_service('test', 'service', '114.212.189.147:2376', 'project')
    # print database_update.service_list('test', 'project')
    # print database_update.delete_service('test', 'project')
    # print database_update.service_list('test', 'project')
    # print database_update.project_list('test', 0, 2)
    # database_update.delete_project('test', 'project')
    # print database_update.project_list('test', 0, 2)
    print database_update.service_ip('test', 'project', 'service')
