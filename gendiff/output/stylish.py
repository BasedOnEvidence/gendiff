from gendiff.constants import (
    ADDED, CHANGED, REMOVED, NESTED
)

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


def stringify_complex_value(node, lines, depth):
    for key in node:
        indent = INDENT_MUL * depth
        if isinstance(node[key], dict):
            lines.append(DATA_OUTPUT_TEMPLATE.format(indent, key, '{'))
            stringify_complex_value(node[key], lines, depth + 1)
            lines.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        else:
            lines.append(
                DATA_OUTPUT_TEMPLATE.format(indent, key, stringify(node[key]))
            )


def build_value(key, value, indent, sign, depth):
    local_output = []
    local_indent = indent[:-2] + sign + ' '
    if isinstance(value, dict):
        local_output.append(
            DATA_OUTPUT_TEMPLATE.format(local_indent, key, '{')
        )
        stringify_complex_value(value, local_output, depth + 1)
        local_indent = indent[:-2] + ' ' + ' '
        local_output.append(END_OUTPUT_TEMPLATE.format(local_indent, '}'))
    else:
        local_output.append(
            DATA_OUTPUT_TEMPLATE.format(
                local_indent,
                key,
                stringify(value)
            )
        )
    return local_output


def inner(diff, output, depth=1):
    for elem in diff:
        indent = depth * INDENT_MUL
        if elem.status == NESTED:
            output.append(DATA_OUTPUT_TEMPLATE.format(indent, elem.key, '{'))
            inner(elem.value, output, depth + 1)
            output.append(END_OUTPUT_TEMPLATE.format(indent, '}'))
        elif elem.status == ADDED:
            output.extend(
                build_value(elem.key, elem.value, indent, '+', depth)
            )
        elif elem.status == REMOVED:
            output.extend(
                build_value(elem.key, elem.value, indent, '-', depth)
            )
        elif elem.status == CHANGED:
            output.extend(
                build_value(elem.key, elem.value[0], indent, '-', depth)
            )
            output.extend(
                build_value(elem.key, elem.value[1], indent, '+', depth)
            )
        else:
            output.extend(
                build_value(elem.key, elem.value, indent, ' ', depth)
            )
    return output


def render(diff):
    result = []
    result.append('{')
    result.extend(inner(diff, []))
    result.append('}')
    return '\n'.join(result)
