from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, DATA_OUTPUT_TEMPLATE, END_OUTPUT_TEMPLATE
)


INDENT_MUL = ' ' * 4


def change_indent_sign(indent, sign=' '):
    return indent[:-2] + sign + ' '


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


def stringify_complex_value(node, lines, depth):
    for key in node:
        indent = depth * INDENT_MUL
        if isinstance(node[key], dict):
            lines.append(DATA_OUTPUT_TEMPLATE.format(indent, key, '{'))
            stringify_complex_value(node[key], lines, depth + 1)
            lines.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        else:
            lines.append(
                DATA_OUTPUT_TEMPLATE.format(indent, key, stringify(node[key]))
            )


def display_value(key, value, indent, output, depth):
    if isinstance(value, dict):
        output.append(DATA_OUTPUT_TEMPLATE.format(indent, key, '{'))
        stringify_complex_value(value, output, depth + 1)
        indent = change_indent_sign(indent)
        output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
    else:
        output.append(
            DATA_OUTPUT_TEMPLATE.format(
                indent,
                key,
                stringify(value)
            )
        )


def inner(diff, output, depth=1):
    for elem in diff:
        indent = depth * INDENT_MUL
        if elem.status == NESTED:
            output.append(DATA_OUTPUT_TEMPLATE.format(indent, elem.key, '{'))
            inner(elem.value, output, depth + 1)
            output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        elif elem.status == ADDED:
            indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value, indent, output, depth)
        elif elem.status == REMOVED:
            indent = change_indent_sign(indent, '-')
            display_value(elem.key, elem.value, indent, output, depth)
        elif elem.status == CHANGED:
            indent = change_indent_sign(indent, '-')
            display_value(elem.key, elem.value[0], indent, output, depth)
            indent = change_indent_sign(indent, '+')
            display_value(elem.key, elem.value[1], indent, output, depth)
        else:
            display_value(elem.key, elem.value, indent, output, depth)


def render(diff):
    output = []
    output.append('{')
    inner(diff, output)
    output.append('}')
    return '\n'.join(output)
