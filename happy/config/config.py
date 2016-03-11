import yaml
import os

def read(file_path):
    if not os.path.isfile(file_path):
        return '-'

    f = open(file_path)
    config = yaml.safe_load(f)

    return config
