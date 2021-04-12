from gendiff.output import stylish, plain, json
DEFAULT_FORMAT = "stylish"


formats = {
    "stylish": stylish.make_stylish,
    "plain": plain.make_plain,
    "json": json.make_json
}


def gen_output(diff, diff_output_format):
    return formats[diff_output_format](diff)
