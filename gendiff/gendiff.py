import bisect
from collections import namedtuple

from gendiff.output.formatters import gen_output
from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME, STYLISH_FORMAT
)
from gendiff.loader import load_file

Node = namedtuple('node', 'key, status, value')


def insert_item(diff, keys, item, current_key):
    insert_position = bisect.bisect_right(keys, current_key)
    keys.insert(insert_position, current_key)
    diff.insert(insert_position, item)


def build_diff_tree(data1, data2):  # noqa: C901
    diff = []
    keys = []
    for key in (data2.keys() - data1.keys()):
        item = Node(key, ADDED, data2[key])
        insert_item(diff, keys, item, key)
    for key in (data1.keys() - data2.keys()):
        item = Node(key, REMOVED, data1[key])
        insert_item(diff, keys, item, key)
    for key in (data1.keys() & data2.keys()):
        if isinstance(data1[key], dict) and isinstance(data2[key], dict):
            item = Node(key, NESTED, build_diff_tree(data1[key], data2[key]))
            insert_item(diff, keys, item, key)
        elif data1[key] == data2[key]:
            item = Node(key, SAME, data2[key])
            insert_item(diff, keys, item, key)
        elif data1[key] != data2[key]:
            item = Node(key, CHANGED, (data1[key], data2[key]))
            insert_item(diff, keys, item, key)
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
