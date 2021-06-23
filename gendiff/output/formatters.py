from gendiff.output import stylish, plain, json
from gendiff.constants import STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT


formats = {
    STYLISH_FORMAT: stylish,
    PLAIN_FORMAT: plain,
    JSON_FORMAT: json
}


def gen_output(diff, format):
    if format in formats:
        return formats[format].render(diff)
    else:
        return 'No such format "{}"! Please use: {}'.format(
            format, ', '.join(formats.keys())
        )
