import json
import yaml

from json.decoder import JSONDecodeError
from yaml.error import YAMLError
from collections import namedtuple


Node = namedtuple('node', 'key, status, value')

formats = {
    '.json': [json.loads, JSONDecodeError],
    '.yml': [yaml.safe_load, YAMLError],
    '.yaml': [yaml.safe_load, YAMLError]
}
