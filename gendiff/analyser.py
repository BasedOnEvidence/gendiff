import json
import yaml
import os


def gen_dict(current_file, keys):
    dict_ = {}
    for key in current_file:
        if key in keys:
            dict_[key] = current_file[key]
    return dict_


def gen_tuple_dict(first_file, second_file, keys):
    dict_ = {}
    for key in first_file:
        if key in keys:
            dict_[key] = (first_file[key], second_file[key])
    return dict_


def gen_str(current_dict, status=" "):
    s = []
    for key in current_dict:
        s.append("  {} {}: {}".format(status, key, current_dict[key]))
    return s


def gen_str_with_diff(current_dict):
    s = []
    for key in current_dict:
        s.append("  {} {}: {}".format("-", key, current_dict[key][0]))
        s.append("  {} {}: {}".format("+", key, current_dict[key][1]))
    return s


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


def generate_diff(file_path1, file_path2):
    first_file = load_file(file_path1)
    second_file = load_file(file_path2)
    removed_keys, same_keys, different_keys, added_keys = (
        get_diff_keys(first_file, second_file)
    )
    dict_of_removed_keys = gen_dict(first_file, removed_keys)
    dict_of_same_keys = gen_dict(first_file, same_keys)
    dict_of_different_keys = (
        gen_tuple_dict(first_file, second_file, different_keys)
    )
    dict_of_added_keys = gen_dict(second_file, added_keys)
    diff = []
    diff.append("{")
    diff.extend(gen_str(dict_of_removed_keys, "-"))
    diff.extend(gen_str(dict_of_same_keys))
    diff.extend(gen_str_with_diff(dict_of_different_keys))
    diff.extend(gen_str(dict_of_added_keys, "+"))
    diff.append("}")
    return "\n".join(diff)
