import argparse
from gendiff.constants import STYLISH_FORMAT
from gendiff.output import output_selector


def get_args_parser():
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f",
                        "--format",
                        choices=output_selector.formats.keys(),
                        default=STYLISH_FORMAT,
                        help="set format of output")
    return parser
