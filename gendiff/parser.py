import json
import yaml


formats = {
    '.json': json.loads,
    '.yml': yaml.safe_load,
    '.yaml': yaml.safe_load
}


def parser(data, extension):
    if extension not in formats.keys():
        raise TypeError(
            "File have to be one of the folowing formats: {}".format(
                formats.keys()
            )
        )
    load_func = formats[extension]
    return load_func(data)
