import json
import yaml

from json.decoder import JSONDecodeError
from yaml.error import YAMLError


formats = {
    'json': [json.loads, JSONDecodeError],
    'yml': [yaml.safe_load, YAMLError],
    'yaml': [yaml.safe_load, YAMLError]
}


def parser(data, extension):
    if extension not in formats.keys():
        raise TypeError(
            'Bad format. The following formats are supported: {}'.format(
                formats.keys()
            )
        )
    load_func, err = formats[extension]
    try:
        data = load_func(data)
    except err:
        raise ValueError('Bad data')
    return data
