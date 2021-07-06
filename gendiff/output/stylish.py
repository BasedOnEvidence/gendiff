from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME
)
from gendiff.structures import Node

INDENT = ' ' * 2


def strignify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def dict_to_nodes(value):
    return [Node(key, SAME, val) for key, val in value.items()]


def strignify_complex_value(key, value, sign, indent):
    return '{}{} {}: {{\n{}\n{}  }}'.format(
        indent, sign, key, value, indent
    )


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
            value = inner(elem.value, indent + 4 * ' ')
            output.append(strignify_complex_value(
                elem.key, value, ' ', indent
            ))
        else:
            sign = {
                ADDED: '+', REMOVED: '-', SAME: ' '
            }[elem.status]
            if isinstance(elem.value, dict):
                value = inner(dict_to_nodes(elem.value), indent + 4 * ' ')
                output.append(strignify_complex_value(
                    elem.key, value, sign, indent
                ))
            else:
                output.append('{}{} {}: {}'.format(
                    indent, sign, elem.key, strignify(elem.value)
                ))
    return '\n'.join(output)


def render(diff):
    return '{\n' + inner(diff) + '\n}'
