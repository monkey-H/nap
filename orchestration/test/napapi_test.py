from orchestration.nap_api import app_info

print app_info.project_list('test', 0, 10)
print app_info.service_list('test', 'test')
