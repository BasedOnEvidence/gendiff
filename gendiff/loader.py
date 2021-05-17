import json
import os
import yaml

from yaml.error import YAMLError


def load_file(file_path):
    with open(file_path, 'r') as file_:
        try:
            if os.path.splitext(file_path)[1] == ".json":
                file_ = json.load(file_)
            elif (os.path.splitext(file_path)[1] == ".yml"
                  or os.path.splitext(file_path)[1] == ".yaml"):
                file_ = yaml.safe_load(file_)
            else:
                print("Plese add .yml or .json to {}".format(file_path))
                file_ = {}
        except YAMLError:
            print("Bad data in {}".format(file_path))
            file_ = {}
    return file_
