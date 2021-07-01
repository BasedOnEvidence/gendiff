from collections import namedtuple

from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED, SAME
)


DATA_OUTPUT_TEMPLATE = '{}{}: {}'
END_OUTPUT_TEMPLATE = '{}{}'

INDENT = ' ' * 2


def strignify(value):
    # Node = namedtuple('node', 'key, status, value')
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def convert(value):
    if isinstance(value, dict):
        Node = namedtuple('node', 'key, status, value')
        structure = []
        for key, val in value.items():
            structure.append(Node(key, SAME, val))
        return structure
    return value


def inner(diff, indent=INDENT, output=[]):  # noqa: C901
    for elem in diff:
        if elem.status == NESTED:
            output.append('{}{} {}: {}'.format(indent, ' ', elem.key, '{'))
            inner(convert(elem.value), indent + 4 * ' ')
            output.append('{}  {}'.format(indent, '}'))
        else:
            if elem.status == CHANGED:
                if isinstance(elem.value[0], dict):
                    output.append(
                        '{}{} {}: {}'.format(indent, '-', elem.key, '{')
                    )
                    inner(convert(elem.value[0]), indent + 4 * ' ')
                    output.append('{}  {}'.format(indent, '}'))
                else:
                    output.append('{}{} {}: {}'.format(
                        indent, '-', elem.key, strignify(elem.value[0])
                    ))
                if isinstance(elem.value[1], dict):
                    output.append(
                        '{}{} {}: {}'.format(indent, '+', elem.key, '{')
                    )
                    inner(convert(elem.value[1]), indent + 4 * ' ')
                    output.append('{}  {}'.format(indent, '}'))
                else:
                    output.append('{}{} {}: {}'.format(
                        indent, '+', elem.key, strignify(elem.value[1])
                    ))
            else:
                sign = {ADDED: '+', REMOVED: '-', SAME: ' '}[elem.status]
                if isinstance(elem.value, dict):
                    output.append(
                        '{}{} {}: {}'.format(indent, sign, elem.key, '{')
                    )
                    inner(convert(elem.value), indent + 4 * ' ')
                    output.append('{}  {}'.format(indent, '}'))
                else:
                    output.append('{}{} {}: {}'.format(
                        indent, sign, elem.key, strignify(elem.value)
                    ))
    return output


def render(diff):
    lst = inner(diff)
    result = '\n'.join(lst)
    lst.clear()
    return '\n'.join(['{', result, '}'])
