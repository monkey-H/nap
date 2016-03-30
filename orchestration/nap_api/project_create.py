# coding=utf-8
from orchestration.database import database_update
import re
import os
import logging
import shutil

from orchestration import config
from orchestration.project import Project

from git import Repo
from git.exc import GitCommandError
from orchestration.database.database_update import roll_back

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


# base_path = '/home/monkey/Documents/filebrowser'
# container_path = '/nap'
# database_url = '114.212.189.147'

# git clone from url into file
def create_project_from_url(username, password, project_name, url):
    if database_update.project_exists(username, password, project_name):
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

    database_update.create_project(username, password, project_name, url)

    return create_project_from_file(username, password, project_name)


def create_project_from_filebrowser(username, password, project_name):
    if database_update.project_exists(username, password, project_name):
        return False, "Project: %s already exists! try another name and try again" % project_name

    database_update.create_project(username, password, project_name, "create from filebrowser")

    return create_project_from_file(username, password, project_name)


# file_path include config.base_path, username, project_name
def create_project_from_file(username, password, project_name):
    argv = get_argv(username, project_name)
    if not len(argv) == 0:
        return 'Argv', argv
    else:
        project_path = config.base_path + '/' + username + '/' + project_name
        return create_project_exceptions(username, password, project_path, project_name)


# file_path as before
def get_argv(username, project_name):
    project_path = config.base_path + '/' + username + '/' + project_name
    original_file = open(project_path + '/docker-compose.yml')
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
    os.remove(project_path + '/docker-compose.yml')
    os.rename(project_path + '/tmp.yml', project_path + '/docker-compose.yml')

    argv = list(set(argv))
    rel = []
    for item in argv:
        rel.append(item.split("##")[1])
    return rel


# file_path as before
def replace_argv(username, password, project_name, argv):
    if not argv:
        return False, 'no argv given'
    else:
        project_path = config.base_path + '/' + username + '/' + project_name
        for item in argv:
            replace_string(project_path, item, argv[item])
        return create_project_exceptions(username, password, project_path, project_name)


def replace_string(file_path, key, value):
    original_file = open(file_path + '/docker-compose.yml')
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
    os.remove(file_path + '/docker-compose.yml')
    os.rename(file_path + '/tmp.yml', file_path + '/docker-compose.yml')


# 注意，old->new 这里的new_main将被替换掉
def create_project_exceptions(username, password, project_path, project_name):
    try:
        print project_path
        project = Project.from_file(username, password, project_path)
        project.start()
        # new_main(project_path, username, password)
    # except KeyboardInterrupt:
    #     logs = roll_back(username, password, project_name)
    #     # shutil.rmtree(project_path)
    #     return False, logs + 'Keyboard Aborting'
    # except (UserError, NoSuchService, ConfigurationError, legacy.LegacyError) as e:
    #     logs = roll_back(username, password, project_name)
    #     # shutil.rmtree(project_path)
    #     return False, logs + e.msg
    except DependencyError as e:
        logs = roll_back(username, password, project_name)
        return False, logs + e.msg
    except ConfigurationError as e:
        logs = roll_back(username, password, project_name)
        # shutil.rmtree(project_path)
        return False, logs + e.msg
    except APIError as e:
        logs = roll_back(username, password, project_name)
        # shutil.rmtree(project_path)
        log.error(e.explanation)
        return False, logs + e.explanation
        # sys.exit(1)
        # except BuildError as e:
        #     logs = roll_back(username, password, project_name)
        #     log.error("Service '%s' failed to build: %s" % (e.service.name, e.reason))
        #     # shutil.rmtree(project_path)
        # return False, logs + "Service '%s' failed to build: %s" % (e.service.name, e.reason)
    # except StreamOutputError as e:
    #     logs = roll_back(username, password, project_name)
    #     log.error(e)
    #     # shutil.rmtree(project_path)
    #     return False, e
    # except NeedsBuildError as e:
    #     logs = roll_back(username, password, project_name)
    #     log.error("Service '%s' needs to be built, but --no-build was passed." % e.service.name)
    #     # shutil.rmtree(project_path)
    #     return False, (logs + "Service '%s' needs to be built, but --no-build was passed." % e.service.name)
    except ReadTimeout:
        logs = roll_back(username, password, project_name)
        # shutil.rmtree(project_path)
        log.error(
            "An HTTP request took too long to complete. Retry with --verbose to obtain debug information.\n"
            "If you encounter this issue regularly because of slow network conditions, consider setting "
            "COMPOSE_HTTP_TIMEOUT to a higher value (current value: )."
        )
        return False, logs + (
            "An HTTP request took too long to complete. Retry with --verbose to obtain debug information.\n"
            "If you encounter this issue regularly because of slow network conditions, consider setting "
            "COMPOSE_HTTP_TIMEOUT to a higher value (current value: )."
        )

    return True, "project create successfully"
