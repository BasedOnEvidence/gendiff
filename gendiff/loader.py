import os
import json
import yaml

from collections import namedtuple
from json.decoder import JSONDecodeError
from yaml.error import YAMLError

Format = namedtuple('format', 'extension, function, error')

formats = [
    Format('.json', json.load, JSONDecodeError),
    Format('.yml', yaml.safe_load, YAMLError),
    Format('.yaml', yaml.safe_load, YAMLError)
]


def load_file(file_path):
    unknown_format_detected = True
    with open(file_path, 'r') as file_:
        for format in formats:
            if os.path.splitext(file_path)[1] == format.extension:
                try:
                    unknown_format_detected = False
                    file_ = format.function(file_)
                except format.error:
                    print("Bad data in {}".format(file_path))
                    file_ = {}
    if unknown_format_detected:
        print("Plese add .yml or .json to {}".format(file_path))
        file_ = {}
    return file_
