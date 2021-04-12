from gendiff.analyser import ADDED, CHANGED, REMOVED, NESTED


ADDED_MSG = "Property {}{} was added with value {}"
REMOVED_MSG = "Property {}{} was removed."
CHANGED_MSG = "Property {}{} was updated. From {} to {}"


def fix_output(value):
    if type(value) == dict:
        return "[complex value]"
    elif type(value) == bool:
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return "'{}'".format(value)


def make_plain(diff, path=""):
    lines = []
    for elem in diff:
        if elem.status == NESTED:
            lines.append(
                make_plain(elem.value, "{}{}.".format(path, elem.key))
            )
        if elem.status == CHANGED:
            lines.append(
                CHANGED_MSG.format(
                    path,
                    elem.key,
                    fix_output(elem.value[0]),
                    fix_output(elem.value[1])
                )
            )
        if elem.status == ADDED:
            lines.append(
                ADDED_MSG.format(
                    path,
                    elem.key,
                    fix_output(elem.value)
                )
            )
        if elem.status == REMOVED:
            lines.append(
                REMOVED_MSG.format(
                    path,
                    elem.key,
                    fix_output(elem.value)
                )
            )
    return '\n'.join(lines)
