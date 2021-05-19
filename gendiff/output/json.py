import json


def render(diff, debug=False):
    return json.dumps(diff, indent=4)
