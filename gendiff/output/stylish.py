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


def inner(diff, output, status, depth=1):
    for elem in diff:
        if status != DICT:
            status = elem.status
        indent = depth * INDENT_MUL
        if status == NESTED:
            output.append(DATA_OUTPUT_TEMPLATE.format(indent, elem.key, '{'))
            inner(elem.value, output, status, depth + 1)
            output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        elif status == DICT:
            if isinstance(diff[elem], dict):
                output.append(DATA_OUTPUT_TEMPLATE.format(indent, elem, '{'))
                inner(diff[elem], output, status, depth + 1)
                output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
            else:
                output.append(
                    build_value(elem, diff[elem], indent, ' ')
                )
        elif status == ADDED:
            if isinstance(elem.value, dict):
                output.append(build_value(elem.key, '{', indent, '+'))
                inner(elem.value, output, DICT, depth + 1)
                output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
            else:
                output.append(
                    build_value(elem.key, elem.value, indent, '+')
                )
        elif status == REMOVED:
            if isinstance(elem.value, dict):
                output.append(build_value(elem.key, '{', indent, '-'))
                inner(elem.value, output, DICT, depth + 1)
                output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
            else:
                output.append(
                    build_value(elem.key, elem.value, indent, '-')
                )
        elif status == CHANGED:
            if isinstance(elem.value[0], dict):
                output.append(build_value(elem.key, '{', indent, '-'))
                inner(elem.value[0], output, DICT, depth + 1)
                output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
            else:
                output.append(
                    build_value(elem.key, elem.value[0], indent, '-')
                )
            if isinstance(elem.value[1], dict):
                output.append(build_value(elem.key, '{', indent, '+'))
                inner(elem.value[1], output, DICT, depth + 1)
                output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
            else:
                output.append(
                    build_value(elem.key, elem.value[1], indent, '+')
                )
        else:
            output.append(build_value(elem.key, elem.value, indent, ' '))
    return output


def render(diff):
    result = []
    result.append('{')
    status = diff[0].status
    result.extend(inner(diff, [], status))
    result.append('}')
    return '\n'.join(result)
