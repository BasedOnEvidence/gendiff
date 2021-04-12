import json


def make_json(diff):
    return json.dumps(diff, sort_keys=True, indent=4)
