import json
import yaml

from json.decoder import JSONDecodeError
from yaml.error import YAMLError

formats = {
    '.json': [json.loads, JSONDecodeError],
    '.yml': [yaml.safe_load, YAMLError],
    '.yaml': [yaml.safe_load, YAMLError]
}


def parser(extension):
    if extension not in formats.keys():
        raise TypeError(
            "File have to be one of the folowing formats: {}".format(
                formats.keys()
            )
        )
