from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME
)
from gendiff.structures import Node

INDENT = ' ' * 2


def gen_output_line(key, value, sign, indent):
    if isinstance(value, bool):
        value = str(value).lower()
    elif value is None:
        value = 'null'
    return ('{}{} {}: {}'.format(
        indent, sign, key, value
    ))


def gen_complex_output_line(key, value, sign, indent):
    return '{}{} {}: {{\n{}\n{}  }}'.format(
        indent, sign, key, value, indent
    )


def dict_to_nodes(value):
    return [Node(key, SAME, val) for key, val in value.items()]


def inner(diff, indent=INDENT):
    output = []
    for elem in diff:
        if elem.status == CHANGED:
            output.append(
                inner([Node(elem.key, REMOVED, elem.value[0])], indent)
            )
            output.append(
                inner([Node(elem.key, ADDED, elem.value[1])], indent)
            )
        elif elem.status == NESTED:
            value = inner(elem.value, indent + ' ' * 4)
            output.append(gen_complex_output_line(
                elem.key, value, ' ', indent
            ))
        else:
            sign = {
                ADDED: '+', REMOVED: '-', SAME: ' '
            }[elem.status]
            if isinstance(elem.value, dict):
                value = inner(dict_to_nodes(elem.value), indent + ' ' * 4)
                output.append(gen_complex_output_line(
                    elem.key, value, sign, indent
                ))
            else:
                output.append(gen_output_line(
                    elem.key, elem.value, sign, indent
                ))
    return '\n'.join(output)


def render(diff):
    return '{\n' + inner(diff) + '\n}'
