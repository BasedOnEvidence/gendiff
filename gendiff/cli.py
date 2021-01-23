import argparse


def user_req_init():
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", dest="format",
                        help="set format of output")
    return parser
