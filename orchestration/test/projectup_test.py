from orchestration.project import Project
from orchestration.database import database_update
import sys
from orchestration.nap_api import project_create

# database_update.create_project('test', 'p1', 'hello from nju')
p = Project.from_file('test', '/home/monkey/Documents/com/p1')

p.create()
p.start()
