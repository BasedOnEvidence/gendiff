from gendiff.constants import (
    STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT
)
from gendiff.gendiff import generate_diff
from gendiff.loader import get_data_from
import json
import pytest


def get_resource_path(file_name):
    return 'tests/fixtures/{}'.format(file_name)


def read(file_name):
    path = get_resource_path(file_name)
    with open(path, 'r') as fixture:
        return fixture.read()


def test_json_load_errors():
    BAD_JSON_EXT = get_resource_path('bad-json-ext')
    BAD_JSON_DATA = get_resource_path('incorrect-json.json')
    with pytest.raises(TypeError):
        get_data_from(BAD_JSON_EXT)
    with pytest.raises(ValueError):
        get_data_from(BAD_JSON_DATA)


def test_output():
    JSON1 = get_resource_path('json1.json')
    JSON2 = get_resource_path('json2.json')
    YML1 = get_resource_path('yml1.yml')
    YML2 = get_resource_path('yml2.yml')
    FULL_JSON1 = get_resource_path('full-json1.json')
    FULL_JSON2 = get_resource_path('full-json2.json')
    FULL_YML1 = get_resource_path('full-yml1.yml')
    FULL_YML2 = get_resource_path('full-yml2.yml')
    assert json.loads(read('expected-json.json')) == (
        json.loads(generate_diff(FULL_JSON1, FULL_JSON2, JSON_FORMAT))
    )
    assert json.loads(read('expected-json.json')) == (
        json.loads(generate_diff(FULL_YML1, FULL_YML2, JSON_FORMAT))
    )
    assert read('jsondiff.txt') == (
        generate_diff(JSON1, JSON2, STYLISH_FORMAT)
    )
    assert read('jsondiff.txt') == (generate_diff(YML1, YML2, STYLISH_FORMAT))
    assert read('jsondiff.txt') == (generate_diff(YML1, JSON2, STYLISH_FORMAT))
    assert read('expected-stylish.txt') == generate_diff(
        FULL_JSON1, FULL_JSON2, STYLISH_FORMAT
    )
    assert read('expected-stylish.txt') == generate_diff(
        FULL_JSON1, FULL_JSON2
    )
    assert read('expected-plain.txt') == generate_diff(
        FULL_JSON1, FULL_JSON2, PLAIN_FORMAT
    )
