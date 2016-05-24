from orchestration.project import Project
from orchestration.database import database_update
import sys
from orchestration.nap_api import project_create
#
# database_update.create_project('test', 'p5', 'hello from nap')
# p = Project.from_file('test', '/home/monkey/Documents/com/p5')
# p.create()
# p.start()
#
#
# database_update.create_project('test', 'p6', 'hello from nap')
# p = Project.from_file('test', '/home/monkey/Documents/com/p6')
# p.create()
# p.start()

database_update.create_project('test', 'pp', 'hello from nap')
p = Project.from_file('test', '/home/monkey/Documents/test')

p.create()
p.start()
