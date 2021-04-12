from gendiff.cli import get_args_parser
from gendiff.analyser import generate_diff
from gendiff.output import output_selector


def gendiff():
    parser = get_args_parser()
    args = parser.parse_args()
    temp_diff = generate_diff(args.first_file, args.second_file)
    diff = output_selector.gen_output(temp_diff, args.format)
    print(diff)
