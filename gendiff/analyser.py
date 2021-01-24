import json


def gen_str(current_file, keys, status=" "):
    s = ""
    for key in keys:
        s += "  {} {}: {}\n".format(status, key, current_file[key])
    return s


def get_keys_status(first_file, second_file):
    first_file_keys = set(first_file.keys())
    second_file_keys = set(second_file.keys())
    added_keys = second_file_keys - first_file_keys
    removed_keys = first_file_keys - second_file_keys
    shared_keys = first_file_keys.intersection(second_file_keys)
    same_keys = set()
    different_keys = set()
    for key in shared_keys:
        if first_file[key] == second_file[key]:
            same_keys.add(key)
        else:
            different_keys.add(key)
    return removed_keys, same_keys, different_keys, added_keys


def generate_diff(file_path1, file_path2):
    first_file = json.load(open(file_path1))
    second_file = json.load(open(file_path2))
    removed_keys, same_keys, different_keys, added_keys = (
        get_keys_status(first_file, second_file)
    )
    diff = "{\n"
    diff += gen_str(first_file, removed_keys, "-")
    diff += gen_str(first_file, same_keys)
    diff += gen_str(first_file, different_keys, "-")
    diff += gen_str(second_file, different_keys, "+")
    diff += gen_str(second_file, added_keys, "+")
    diff += "}"
    return diff
