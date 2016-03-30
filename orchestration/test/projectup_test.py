from orchestration.project import Project
from orchestration.database import database_update
import sys

database_update.create_project('test', 'test', 'hello from nju')
p = Project.from_file('test', '/home/monkey/Documents/just4happy/orchestration/test')

p.create()
p.start()
