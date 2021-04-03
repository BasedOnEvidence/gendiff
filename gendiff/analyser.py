import json
import os

import yaml


def gen_dict(current_dict, keys, status):
    res_dict = {}
    for key in current_dict:
        if key in keys:
            res_dict[key] = current_dict[key]
            res_dict[key].append(status)
    return res_dict


def gen_tuple_dict(first_file, second_file, keys, status):
    res_dict = {}
    for key in first_file:
        if key in keys:
            res_dict[key] = [(first_file[key], second_file[key]), status]
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
            res_dict[os.path.join(path, elem_key) + '/'] = ["VALUE",
                                                            src_dict[elem_key]]
    return res_dict


def generate_diff(file_path1, file_path2):
    first_data = load_file(file_path1)
    second_data = load_file(file_path2)
    first_dict = gen_depth_dict(first_data, {})
    second_dict = gen_depth_dict(second_data, {})
    removed_keys, same_keys, different_keys, added_keys = (
        get_diff_keys(first_dict, second_dict)
    )
    dict_of_removed_keys = gen_dict(first_dict, removed_keys, "REMOVED")
    dict_of_same_keys = gen_dict(first_dict, same_keys, "SAME")
    dict_of_different_keys = (
        gen_tuple_dict(first_dict, second_dict, different_keys, "CHANGED")
    )
    dict_of_added_keys = gen_dict(second_dict, added_keys, "ADDED")
    result_dict = {}
    result_dict.update(dict_of_removed_keys)
    result_dict.update(dict_of_same_keys)
    result_dict.update(dict_of_different_keys)
    result_dict.update(dict_of_added_keys)
    return result_dict
