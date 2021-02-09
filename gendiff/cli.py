import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", dest="format",
                        help="set format of output")
    return parser
