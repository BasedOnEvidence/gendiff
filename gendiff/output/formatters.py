from gendiff.output import stylish, plain, json
from gendiff.constants import STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT


ERROR_MESSAGE = 'No such format "{}"! Please use "{}", "{}" or "{}"'


formats = {
    STYLISH_FORMAT: stylish,
    PLAIN_FORMAT: plain,
    JSON_FORMAT: json
}


def gen_output(diff, format):
    try:
        return formats[format].render(diff)
    except KeyError:
        return ERROR_MESSAGE.format(format,
                                    STYLISH_FORMAT,
                                    PLAIN_FORMAT,
                                    JSON_FORMAT)
