from collections import namedtuple
from operator import attrgetter

from gendiff.output.formatters import gen_output
from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME, STYLISH_FORMAT
)
from gendiff.loader import load_file

Node = namedtuple('node', 'key, status, value')


def build_diff_tree(data1, data2):
    diff = []
    for key in (data2.keys() - data1.keys()):
        diff.append(Node(key, ADDED, data2[key]))
    for key in (data1.keys() - data2.keys()):
        diff.append(Node(key, REMOVED, data1[key]))
    for key in (data1.keys() & data2.keys()):
        if isinstance(data1[key], dict) and isinstance(data2[key], dict):
            diff.append(
                Node(key, NESTED, build_diff_tree(data1[key], data2[key]))
            )
        elif data1[key] == data2[key]:
            diff.append(Node(key, SAME, data2[key]))
        else:
            diff.append(Node(key, CHANGED, (data1[key], data2[key])))
        diff.sort(key=attrgetter('key'))
    return diff


def generate_diff(
    first_file, second_file,
    style=STYLISH_FORMAT
):
    first_data = load_file(first_file)
    second_data = load_file(second_file)
    diff = build_diff_tree(first_data, second_data)
    diff = gen_output(diff, style)
    return diff
