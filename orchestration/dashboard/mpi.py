from orchestration import config
from orchestration.nap_api import create_from_table
from orchestration.nap_api import app_info

def create_mpi(username, password, mpi_name, slaves):
    table = []
    args = {'type':'mpi', 'slaves':slaves}
    table.append(args)
    print app_info.destroy_project(username, password, mpi_name)
    print create_from_table.create_project_from_table(username, password, mpi_name, table)
