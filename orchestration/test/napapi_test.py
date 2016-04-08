from __future__ import print_function
from __future__ import print_function
from orchestration.nap_api import app_info

# print(app_info.project_list('test', 0, 10))
# print(app_info.service_list('test', 'project'))
#
# app_info.destroy_project('test', 'test')
#
# print(app_info.project_list('test', 0, 10))
# print(app_info.service_list('test', 'test'))

# print (app_info.get_logs('test', 'p1', 'master'))
# print (app_info.get_project('test', 'p1'))
print (app_info.get_service('test', 'p1', 'master'))

print (app_info.kill_project('test', 'p1'))
print (app_info.get_service('test', 'p1', 'master'))

print (app_info.restart_project('test', 'p1'))
print (app_info.get_service('test', 'p1', 'master'))
