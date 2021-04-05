import json
import os

import yaml


def gen_dict(current_dict, keys, status):
    res_dict = {}
    for key in current_dict:
        if key in keys:
            if current_dict[key] == ["KEY"]:
                res_dict[key] = ["KEY", status]
            else:
                res_dict[key] = ["VALUE", current_dict[key], status]
    return res_dict


def gen_tuple_dict(first_file, second_file, keys, status):
    res_dict = {}
    for key in first_file:
        if key in keys:
            res_dict[key] = [
                "VALUE", (first_file[key], second_file[key]), status
            ]
    return res_dict


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


def gen_depth_dict(src_dict, res_dict={}, path=''):
    for elem_key in src_dict:
        if type(src_dict[elem_key]) == dict:
            res_dict[os.path.join(path, elem_key) + '/'] = ["KEY"]
            gen_depth_dict(
                src_dict[elem_key], res_dict, os.path.join(path, elem_key)
            )
        else:
            res_dict[os.path.join(path, elem_key) + '/'] = src_dict[elem_key]
    return res_dict


def get_diff_on_next_layer(layer_diff, key, data1, data2, last_status=""):
    if type(data1) == dict and type(data2) == dict:
        next_layer_diff = get_diff_on_current_layer(data1, data2)
        layer_diff.append(
            {"key": key,
             "status": "UNKNOWN",
             "value": next_layer_diff}
        )
    else:
        if data1 == data2:
            layer_diff.append(
                {"key": key,
                 "status": "SAME",
                 "value": data2}
            )
        # Если сравнивать словарь-значение, то все равно changed
        if data1 != data2:
            layer_diff.append(
                {"key": key,
                 "status": "CHANGED",
                 "value": (data1, data2)}
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
        diff.append({"key": key, "status": "ADDED", "value": data2[key]})
    for key in removed_keys:
        diff.append({"key": key, "status": "REMOVED", "value": data1[key]})
    return diff


def generate_diff(file_path1, file_path2):
    first_data = load_file(file_path1)
    second_data = load_file(file_path2)
    diff = get_diff_on_current_layer(first_data, second_data)
    # print(diff)
    print(json.dumps(diff, sort_keys=True, indent=4))
    return diff
