from operator import attrgetter
from collections import namedtuple

from gendiff.output.output_selector import gen_output
from gendiff.constants import ADDED, CHANGED, REMOVED, NESTED, SAME, \
    STYLISH_FORMAT
from gendiff.loader import load_file

Node = namedtuple("node", "key, status, value")


def get_diff_on_next_layer(diff, key, data1, data2):
    if type(data1) == dict and type(data2) == dict:
        diff.append(Node(key, NESTED, build_diff_tree(data1, data2)))
    else:
        if data1 == data2:
            diff.append(Node(key, SAME, data2))
        # Если сравнивать словарь-значение, то все равно changed
        if data1 != data2:
            diff.append(Node(key, CHANGED, (data1, data2)))


def build_diff_tree(data1, data2):
    added_keys = data2.keys() - data1.keys()
    removed_keys = data1.keys() - data2.keys()
    shared_keys = data1.keys() & data2.keys()
    diff = []
    # Если ключ не общий, то на уровнях ниже разницы не существует
    for key in added_keys:
        diff.append(Node(key, ADDED, data2[key]))
    for key in removed_keys:
        diff.append(Node(key, REMOVED, data1[key]))
    for key in shared_keys:
        get_diff_on_next_layer(diff, key, data1[key], data2[key])
        diff.sort(key=attrgetter("key"))
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
