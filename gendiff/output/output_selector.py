from gendiff.output import stylish

DEFAULT_FORMAT = "stylish"


formats = {
    "stylish": stylish.make_stylish
}


def gen_output(diff, diff_output_format):
    return formats[diff_output_format](diff)
