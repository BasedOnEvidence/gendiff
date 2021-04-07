import os
from gendiff.analyser import ADDED, CHANGED, REMOVED, NESTED

INDENT_MUL = ' ' * 4


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


def change_indent_sign(indent, sign=' '):
    return indent[:-2] + sign + ' '


def display_complex_value(node, depth):
    for key in node:
        indent = depth * INDENT_MUL
        if type(node[key]) == dict:
            print("{}{}: {}".format(indent, key, '{'))
            display_complex_value(node[key], depth + 1)
            print("{}{}".format(indent, '}'))
        else:
            print(
                "{}{}: {}".format(indent, key, node[key])
            )


def display_value(key, value, indent, depth):
    if type(value) == dict:
        print("{}{}: {}".format(indent, key, '{'))
        display_complex_value(value, depth + 1)
        indent = change_indent_sign(indent)
        print("{}{}".format(indent, '}'))
    else:
        print(
            "{}{}: {}".format(
                indent,
                key,
                value
            )
        )


def display_as_stylish(diff, depth=1):
    for elem in diff:
        indent = depth * INDENT_MUL
        if elem.status == NESTED:
            print("{}{}: {}".format(indent, elem.key, '{'))
            display_as_stylish(elem.value, depth + 1)
            print("{}{}".format(indent, '}'))
        elif elem.status == ADDED or elem.status == REMOVED:
            indent = change_indent_sign(indent, '-')
            if elem.status == ADDED:
                indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value, indent, depth)
        elif elem.status == CHANGED:
            indent = change_indent_sign(indent, '-')
            display_value(elem.key, elem.value[0], indent, depth)
            indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value[1], indent, depth)
        else:
            display_value(elem.key, elem.value, indent, depth)


def make_stylish(diff):
    print('{')
    display_as_stylish(diff)
    print('}')
    # container = build_nested(diff.keys())
    # fill_template(container, diff)
    # print(json.dumps(container, sort_keys=True, indent=4))
    # print(json.dumps(res_dict, sort_keys=True, indent=4))
