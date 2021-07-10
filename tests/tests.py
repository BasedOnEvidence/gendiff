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


@pytest.mark.parametrize('extension', ['json', 'yml'])
def test_json_load_errors(extension):
    BAD_EXT = get_resource_path('bad-{}-ext'.format(extension))
    BAD_DATA = get_resource_path('incorrect-{0}.{0}'.format(extension))
    with pytest.raises(TypeError):
        get_data_from(BAD_EXT)
    with pytest.raises(ValueError):
        get_data_from(BAD_DATA)


@pytest.mark.parametrize('extension', ['json', 'yml'])
def test_output(extension):
    SIMPLE_DATA1 = get_resource_path('{0}1.{0}'.format(extension))
    SIMPLE_DATA2 = get_resource_path('{0}2.{0}'.format(extension))
    COMPLEX_DATA1 = get_resource_path('full-{0}1.{0}'.format(extension))
    COMPLEX_DATA2 = get_resource_path('full-{0}2.{0}'.format(extension))
    assert read('jsondiff.txt') == generate_diff(
        SIMPLE_DATA1, SIMPLE_DATA2
    )
    assert read('expected-stylish.txt') == generate_diff(
        COMPLEX_DATA1, COMPLEX_DATA2, STYLISH_FORMAT
    )
    assert read('expected-plain.txt') == generate_diff(
        COMPLEX_DATA1, COMPLEX_DATA2, PLAIN_FORMAT
    )
    assert json.loads(read('expected-json.json')) == (
        json.loads(generate_diff(COMPLEX_DATA1, COMPLEX_DATA2, JSON_FORMAT))
    )
