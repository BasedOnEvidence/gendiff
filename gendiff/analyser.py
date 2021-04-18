import json
import os
import yaml
from operator import attrgetter
from collections import namedtuple

ADDED = "added"
CHANGED = "changed"
REMOVED = "removed"
NESTED = "nested"
SAME = "same"

node = namedtuple("node", "key, status, value")


def get_diff_keys(first_file, second_file):
    first_file_keys = first_file.keys()  # set(first_file.keys())
    second_file_keys = second_file.keys()  # set(second_file.keys())
    added_keys = second_file_keys - first_file_keys
    removed_keys = first_file_keys - second_file_keys
    shared_keys = first_file_keys & second_file_keys
    same_keys = set()
    different_keys = set()
    for key in shared_keys:
        if first_file[key] == second_file[key]:
            same_keys.add(key)
        else:
            different_keys.add(key)
    return removed_keys, same_keys, different_keys, added_keys


def load_file(file_path):
    with open(file_path, 'r') as file_:
        if os.path.splitext(file_path)[1] == ".json":
            file_ = json.load(file_)
        elif os.path.splitext(file_path)[1] == ".yml":
            file_ = yaml.safe_load(file_)
        else:
            print("Plese add .yml or .json to {}".format(file_path))
            file_ = {}
    return file_


def get_diff_on_next_layer(layer_diff, key, data1, data2):
    if type(data1) == dict and type(data2) == dict:
        next_layer_diff = get_diff_on_current_layer(data1, data2)
        layer_diff.append(
            node(key, NESTED, next_layer_diff)
        )
    else:
        if data1 == data2:
            layer_diff.append(
                node(key, SAME, data2)
            )
        # Если сравнивать словарь-значение, то все равно changed
        if data1 != data2:
            layer_diff.append(
                node(key, CHANGED, (data1, data2))
            )


def get_diff_on_current_layer(data1, data2):
    added_keys = data2.keys() - data1.keys()
    removed_keys = data1.keys() - data2.keys()
    shared_keys = data1.keys() & data2.keys()
    diff = []
    for key in shared_keys:
        get_diff_on_next_layer(diff, key, data1[key], data2[key])
    # Если ключ не общий, то на уровнях ниже разницы не существует
    for key in added_keys:
        diff.append(node(key, ADDED, data2[key]))
    for key in removed_keys:
        diff.append(node(key, REMOVED, data1[key]))
    return diff


def sort_dict(node):
    result = {}
    for key, value in sorted(node.items()):
        if type(value) == dict:
            result[key] = sort_dict(value)
        else:
            result[key] = value
    return result


def sort_diff(node):
    node.sort(key=attrgetter("key"))
    for elem in node:
        if type(elem.value) == list:
            sort_diff(elem.value)
        elif type(elem.value) == dict:
            sort_dict(elem.value)
        else:
            pass
    return node


def generate_temp_diff(file_path1, file_path2):
    first_data = load_file(file_path1)
    second_data = load_file(file_path2)
    diff = get_diff_on_current_layer(first_data, second_data)
    diff = sort_diff(diff)
    # print(diff)
    # print(json.dumps(diff, indent=4))
    return diff
