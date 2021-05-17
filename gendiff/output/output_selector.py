from gendiff.output import stylish, plain, json
from gendiff.constants import STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT

formats = {
    STYLISH_FORMAT: stylish.make_stylish,
    PLAIN_FORMAT: plain.make_plain,
    JSON_FORMAT: json.make_json
}


def gen_output(diff, diff_output_format):
    if diff_output_format in formats.keys():
        return formats[diff_output_format](diff)
    return None
