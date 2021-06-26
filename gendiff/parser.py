import json
import yaml

from json.decoder import JSONDecodeError
from yaml.error import YAMLError

formats = {
    '.json': [json.loads, JSONDecodeError],
    '.yml': [yaml.safe_load, YAMLError],
    '.yaml': [yaml.safe_load, YAMLError]
}


def parser(data, extension, file_path):
    if extension in formats.keys():
        load_func, err = formats[extension]
        try:
            data = load_func(data)
        except err:
            raise ValueError("Bad data in {}".format(file_path))
    else:
        raise TypeError(
            "File have to be one of the folowing formats: {}".format(
                formats.keys()
            )
        )
    return data
