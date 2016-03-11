from happy.config import config
import os
import sys

def main():
    f = 'test.yml'
    path = os.path.split(os.path.realpath(__file__))[0]
    file_path = path + '/' + f
    # print file_path

    srv_dicts = config.read(path + '/' + f)
    # print srv_dicts

if __name__ == "__main__":
    main()
