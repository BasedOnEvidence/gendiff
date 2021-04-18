from gendiff.output import stylish, plain, json
DEFAULT_FORMAT = "stylish"
STYLISH_FORMAT = "stylish"
PLAIN_FORMAT = "plain"
JSON_FORMAT = "json"


formats = {
    STYLISH_FORMAT: stylish.make_stylish,
    PLAIN_FORMAT: plain.make_plain,
    JSON_FORMAT: json.make_json
}


def gen_output(diff, diff_output_format):
    return formats[diff_output_format](diff)
