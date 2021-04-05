import os


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


def fill_template(container, src_dict, path=''):
    for elem_key in container:
        new_path = os.path.join(path, elem_key) + '/'
        if container[elem_key] != {}:
            fill_template(container[elem_key], src_dict, new_path)
        else:
            container[elem_key] = src_dict[new_path][1]
    return container


def make_stylish(diff):
    pass
    # container = build_nested(diff.keys())
    # fill_template(container, diff)
    # print(json.dumps(container, sort_keys=True, indent=4))
    # print(json.dumps(res_dict, sort_keys=True, indent=4))
