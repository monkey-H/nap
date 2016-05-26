# coding=utf-8
from orchestration.database import database_update
import re
import os
import logging
import shutil

from orchestration import config
from orchestration.project import Project

from git import Repo #pip pygit
from git.exc import GitCommandError
# from orchestration.database.database_update import roll_back

# from orchestration.config.errors import ComposeFileNotFound
# from orchestration.cli.docopt_command import NoSuchCommand
# from orchestration.cli.errors import UserError
# from orchestration.service import NeedsBuildError
# from orchestration.service import BuildError
# from orchestration.project import ConfigurationError
# from orchestration.project import NoSuchService
# from orchestration.progress_stream import StreamOutputError
# from orchestration.const import HTTP_TIMEOUT

from orchestration.exception import ConfigurationError
from orchestration.exception import DependencyError
from docker.errors import APIError
from requests.exceptions import ReadTimeout

log = logging.getLogger(__name__)


def create_project_from_table(username, project_name, table):
    if database_update.project_exists(username, project_name):
        return False, "Project: %s already exists! try another name and try again" % project_name

    if os.path.exists('%s/%s/%s' % (config.base_path, username, project_name)):
        return False, "File: %s already exists! try another name and try again" % project_name

    os.mkdir("%s/%s/%s" % (config.base_path, username, project_name))
    project_path = config.base_path + '/' + username + '/' + project_name

    database_update.create_project(username, project_name, 'create from table')

    return create_project_exceptions(username, project_path, table, project_name, 'table')


# git clone from url into file
def create_project_from_url(username, project_name, url):
    if database_update.project_exists(username, project_name):
        return False, "Project: %s already exists! try another name and try again" % project_name

    if os.path.exists('%s/%s/%s' % (config.base_path, username, project_name)):
        return False, "File: %s already exists! try another name and try again" % project_name

    os.mkdir("%s/%s/%s" % (config.base_path, username, project_name))
    project_path = config.base_path + '/' + username + '/' + project_name

    try:
        Repo.clone_from(url, project_path)
    except GitCommandError:
        shutil.rmtree(project_path)
        return False, "git command error, please check url: %s" % url
    # except:
    #     return False, "git clone error, please connect administrator for information"

    database_update.create_project(username, project_name, url)

    return create_project_from_file(username, project_name)


def create_project_from_file_browser(username, project_name):
    if database_update.project_exists(username, project_name):
        return False, "Project: %s already exists! try another name and try again" % project_name

    url = "create from file browser"
    database_update.create_project(username, project_name, url)

    return create_project_from_file(username, project_name)


# file_path include config.base_path, username, project_name
def create_project_from_file(username, project_name):
    argv = get_argv(username, project_name)
    if not len(argv) == 0:
        return 'Argv', argv
    else:
        project_path = config.base_path + '/' + username + '/' + project_name
        return create_project_exceptions(username, project_path, None, project_name, 'file')


# file_path as before
def get_argv(username, project_name):
    project_path = config.base_path + '/' + username + '/' + project_name
    original_file = open(project_path + '/nap-compose.yml')
    temp_file = open(project_path + '/tmp.yml', 'w')

    argv = []
    while 1:
        line = original_file.readline()
        if not line:
            break
        if '%%PATH%%' in line:
            line = line.replace('%%PATH%%', config.container_path + '/' + project_name)
        if '##' in line:
            data = re.findall('##.+?##', line)
            if data:
                argv = argv + data
        temp_file.write(line)

    original_file.close()
    temp_file.close()
    os.remove(project_path + '/nap-compose.yml')
    os.rename(project_path + '/tmp.yml', project_path + '/nap-compose.yml')

    argv = list(set(argv))
    rel = []
    for item in argv:
        rel.append(item.split("##")[1])
    return rel


# file_path as before
def replace_argv(username, project_name, argv):
    if not argv:
        return False, 'no argv given'
    else:
        project_path = config.base_path + '/' + username + '/' + project_name
        for item in argv:
            replace_string(project_path, item, argv[item])
        return create_project_exceptions(username, project_path, None, project_name, 'file')


def replace_string(file_path, key, value):
    original_file = open(file_path + '/nap-compose.yml')
    temp_file = open(file_path + '/tmp.yml', 'w')
    while 1:
        line = original_file.readline()
        if not line:
            break
        if key in line:
            line = line.replace('##' + key + '##', value)
        temp_file.write(line)
    original_file.close()
    temp_file.close()
    os.remove(file_path + '/nap-compose.yml')
    os.rename(file_path + '/tmp.yml', file_path + '/nap-compose.yml')


def create_project_exceptions(username, project_path, table, project_name, create_flag):
    try:
        if create_flag == 'file':
            project = Project.from_file(username, project_path)
        else:
            project = Project.from_table(username, project_name, table)
        project.create()
        project.start()
    except DependencyError as e:
        # logs = roll_back(username, project_name)
        # return False, logs + e.msg
        return False, e.msg
    except ConfigurationError as e:
        # logs = roll_back(username, project_name)
        # shutil.rmtree(project_path)
        # return False, logs + e.msg
        return False, e.msg
    except APIError as e:
        # logs = roll_back(username, project_name)
        # shutil.rmtree(project_path)
        log.error(e.explanation)
        # return False, logs + e.explanation
        return False, e.explanation
    except ReadTimeout:
        # logs = roll_back(username, project_name)
        # shutil.rmtree(project_path)
        log.error(
            "An HTTP request took too long to complete. Retry with --verbose to obtain debug information.\n"
            "If you encounter this issue regularly because of slow network conditions, consider setting "
            "COMPOSE_HTTP_TIMEOUT to a higher value (current value: )."
        )
        return False, (
            "An HTTP request took too long to complete. Retry with --verbose to obtain debug information.\n"
            "If you encounter this issue regularly because of slow network conditions, consider setting "
            "COMPOSE_HTTP_TIMEOUT to a higher value (current value: )."
        )

    return True, "project create successfully"
