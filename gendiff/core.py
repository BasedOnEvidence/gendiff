from gendiff.cli import get_args_parser
from gendiff.analyser import generate_diff
from gendiff.output import output_selector


def gendiff():
    parser = get_args_parser()
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    output_selector.gen_output(diff, args.format)
