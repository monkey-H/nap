
log_path='/home/monkey/Documents/filebrowser/logspout_log/syslog'
def get_log(user_name, project_name):
    file = open(log_path)

    container_name = user_name + '-' + project_name
    log_str = ''

    while 1:
        line = file.readline()
        if not line:
            break;
        if container_name in line:
            log_str = log_str + line + '\n'
    file.close()
    return log_str

print get_log('orange', 'java')
