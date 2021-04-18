#!/usr/bin/env python3
from gendiff.core import gendiff
from gendiff.cli import get_args_parser


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    diff = gendiff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == "__main__":
    main()
