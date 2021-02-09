from gendiff.cli import get_args_parser
from gendiff.analyser import generate_diff


def gendiff():
    parser = get_args_parser()
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
