import json


def render(diff):
    return json.dumps(diff, indent=4)
