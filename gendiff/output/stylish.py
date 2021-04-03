import json


def build_nested_helper(path, text, container):
    segs = path.split('/')
    head = segs[0]
    tail = segs[1:]
    if tail:
        if head not in container:
            container[head] = {}
        build_nested_helper('/'.join(tail), text, container[head])


def build_nested(paths):
    container = {}
    for path in paths:
        build_nested_helper(path, path, container)
    return container


def make_stylish(result_dict):
    container = build_nested(result_dict.keys())
    print(json.dumps(container, sort_keys=True, indent=4))
    # keys_list = sorted(keys_status.keys())
    # print(keys_list)
    # print(json.dumps(result_dict, sort_keys=True, indent=4))
