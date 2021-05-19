from gendiff.output import stylish, plain, json
from gendiff.constants import STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT

formatters = {
    STYLISH_FORMAT: stylish,
    PLAIN_FORMAT: plain,
    JSON_FORMAT: json
}


def gen_output(diff, format):
    try:
        return formatters[format].render(diff)
    except KeyError:
        return 'No such format!'
