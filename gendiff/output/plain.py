from gendiff.constants import ADDED, CHANGED, REMOVED, NESTED


ADDED_MSG = "Property '{}{}' was added with value: {}"
REMOVED_MSG = "Property '{}{}' was removed"
CHANGED_MSG = "Property '{}{}' was updated. From {} to {}"


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


def render(diff, path=''):
    lines = []
    for elem in diff:
        if elem.status == NESTED:
            lines.append(
                render(elem.value, '{}{}.'.format(path, elem.key))
            )
        if elem.status == CHANGED:
            lines.append(
                CHANGED_MSG.format(
                    path,
                    elem.key,
                    stringify(elem.value[0]),
                    stringify(elem.value[1])
                )
            )
        if elem.status == ADDED:
            lines.append(
                ADDED_MSG.format(
                    path,
                    elem.key,
                    stringify(elem.value)
                )
            )
        if elem.status == REMOVED:
            lines.append(
                REMOVED_MSG.format(
                    path,
                    elem.key,
                    stringify(elem.value)
                )
            )
    return '\n'.join(lines)
