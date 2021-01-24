from gendiff.cli import user_req_init
from gendiff.analyser import generate_diff


def gendiff():
    parser = user_req_init()
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
