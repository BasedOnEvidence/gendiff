from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED
)

DICT = 'dict'

DATA_OUTPUT_TEMPLATE = '{}{}: {}'
END_OUTPUT_TEMPLATE = '{}{}'

INDENT_MUL = ' ' * 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


def build_value(key, value, indent, sign):
    local_indent = indent[:-2] + sign + ' '
    return (
        DATA_OUTPUT_TEMPLATE.format(
            local_indent,
            key,
            stringify(value)
        )
    )


def build_list(output, key, value, indent, depth, sign=' '):
    if isinstance(value, dict):
        output.append(build_value(key, '{', indent, sign))
        inner(value, output, DICT, depth + 1)
        output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
    else:
        output.append(
            build_value(key, value, indent, sign)
        )


def inner(diff, output, status, depth=1):
    indent = depth * INDENT_MUL
    for elem in diff:
        if status != DICT:
            status = elem.status
        if status == NESTED:
            output.append(build_value(elem.key, '{', indent, ' '))
            inner(elem.value, output, status, depth + 1)
            output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        elif status == DICT:
            build_list(output, elem, diff[elem], indent, depth, ' ')
        elif status == ADDED:
            build_list(output, elem.key, elem.value, indent, depth, '+')
        elif status == REMOVED:
            build_list(output, elem.key, elem.value, indent, depth, '-')
        elif status == CHANGED:
            build_list(output, elem.key, elem.value[0], indent, depth, '-')
            build_list(output, elem.key, elem.value[1], indent, depth, '+')
        else:
            build_list(output, elem.key, elem.value, indent, depth, ' ')
    return output


def render(diff):
    result = []
    result.append('{')
    status = diff[0].status
    result.extend(inner(diff, [], status))
    result.append('}')
    return '\n'.join(result)
