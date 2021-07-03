from operator import attrgetter

from gendiff.output.formatters import gen_output
from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME, STYLISH_FORMAT
)
from gendiff.loader import get_data_from
from gendiff.structures import Node


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
    first_data = get_data_from(first_file)
    second_data = get_data_from(second_file)
    return gen_output(build_diff_tree(first_data, second_data), style)
