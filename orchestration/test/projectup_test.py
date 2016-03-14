from orchestration.project import Project
import sys

p = Project.from_file('hello', 'nju', sys.path[0])

print p.services[0].cont.service
