from gendiff.constants import ADDED, CHANGED, REMOVED, NESTED


def stringify(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return "'{}'".format(value)
    else:
        return value


def inner(diff, path=''):
    lines = []
    for elem in diff:
        if elem.status == NESTED:
            lines.append(
                inner(elem.value, '{}{}.'.format(path, elem.key))
            )
        if elem.status == CHANGED:
            lines.append(
                "Property '{}{}' was updated. From {} to {}".format(
                    path,
                    elem.key,
                    stringify(elem.value[0]),
                    stringify(elem.value[1])
                )
            )
        if elem.status == ADDED:
            lines.append(
                "Property '{}{}' was added with value: {}".format(
                    path,
                    elem.key,
                    stringify(elem.value)
                )
            )
        if elem.status == REMOVED:
            lines.append(
                "Property '{}{}' was removed".format(
                    path,
                    elem.key
                )
            )
    return '\n'.join(lines)


def render(diff):
    return inner(diff)
