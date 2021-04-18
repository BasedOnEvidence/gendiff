#!/usr/bin/env python3
from gendiff.cli import get_args_parser
from gendiff.gendiff import generate_diff


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == "__main__":
    main()
