from gendiff.constants import ADDED, CHANGED, REMOVED, NESTED


INDENT_MUL = ' ' * 4


def change_indent_sign(indent, sign=' '):
    return indent[:-2] + sign + ' '


def fix_output(value):
    if type(value) == bool:
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return value


def display_complex_value(node, lines, depth):
    for key in node:
        indent = depth * INDENT_MUL
        if type(node[key]) == dict:
            lines.append("{}{}: {}".format(indent, key, '{'))
            display_complex_value(node[key], lines, depth + 1)
            lines.append("{}{}".format(indent, '}'))
        else:
            lines.append(
                "{}{}: {}".format(indent, key, fix_output(node[key]))
            )


def display_value(key, value, indent, lines, depth):
    if type(value) == dict:
        lines.append("{}{}: {}".format(indent, key, '{'))
        display_complex_value(value, lines, depth + 1)
        indent = change_indent_sign(indent)
        lines.append("{}{}".format(indent, '}'))
    else:
        lines.append(
            "{}{}: {}".format(
                indent,
                key,
                fix_output(value)
            )
        )


def display_as_stylish(diff, lines, depth=1):
    for elem in diff:
        indent = depth * INDENT_MUL
        if elem.status == NESTED:
            lines.append("{}{}: {}".format(indent, elem.key, '{'))
            display_as_stylish(elem.value, lines, depth + 1)
            lines.append("{}{}".format(indent, '}'))
        elif elem.status == ADDED or elem.status == REMOVED:
            indent = change_indent_sign(indent, '-')
            if elem.status == ADDED:
                indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value, indent, lines, depth)
        elif elem.status == CHANGED:
            indent = change_indent_sign(indent, '-')
            display_value(elem.key, elem.value[0], indent, lines, depth)
            indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value[1], indent, lines, depth)
        else:
            display_value(elem.key, elem.value, indent, lines, depth)


def make_stylish(diff):
    lines = []
    lines.append("{")
    display_as_stylish(diff, lines)
    lines.append("}")
    return '\n'.join(lines)
    # container = build_nested(diff.keys())
    # fill_template(container, diff)
    # print(json.dumps(container, sort_keys=True, indent=4))
    # print(json.dumps(res_dict, sort_keys=True, indent=4))
