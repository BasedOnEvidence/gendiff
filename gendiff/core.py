from gendiff.cli import user_req_init


def gendiff():
    parser = user_req_init()
    args = parser.parse_args()
    print(args)
