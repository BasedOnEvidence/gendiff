import os
import json
import yaml

from collections import namedtuple
from json.decoder import JSONDecodeError
from yaml.error import YAMLError

Format = namedtuple('format', 'extension, function, error')

formats = [
    Format('.json', json.loads, JSONDecodeError),
    Format('.yml', yaml.safe_load, YAMLError),
    Format('.yaml', yaml.safe_load, YAMLError)
]


def parser(data, extension, file_path):
    unknown_format_detected = True
    for format in formats:
        if extension == format.extension:
            unknown_format_detected = False
            try:
                data = format.function(data)
            except format.error:
                raise ValueError("Bad data in {}".format(file_path))
    if unknown_format_detected:
        raise TypeError(
            "File have to be one of the folowing formats: {}".format(
                [item.extension for item in formats]
            )
        )
    return data


def load_file(file_path):
    extension = os.path.splitext(file_path)[1]
    with open(file_path, 'r') as file_:
        return parser(file_.read(), extension, file_path)
