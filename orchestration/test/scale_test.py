from orchestration.dynamic_scalability import server
from orchestration.database import database_update

# server.scale_up('test', 'pear', 'web')
# server.scale_down('test', 'nju', 'web')

# print (server.service_load_calculate('test', 'nju', 'web'))

# print (database_update.create_service_for_scale('test', 'banana', 'web'))
# print (database_update.delete_service_for_scale('test', 'nju', 'web'))
# print (database_update.get_service_for_scale())

server.monitor_scale_service()