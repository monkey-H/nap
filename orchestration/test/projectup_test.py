from orchestration.project import Project
from orchestration.database import database_update
import sys
from orchestration.nap_api import project_create

database_update.create_project('test', 'p2', 'hello from nap')
p = Project.from_file('test', '/home/monkey/Documents/com/p2')

p.create()
p.start()
