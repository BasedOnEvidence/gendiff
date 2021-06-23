from gendiff.constants import (
    STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT
)
from gendiff.gendiff import generate_diff
from gendiff.loader import load_file
import json
import pytest


# Paths
JSON1 = 'tests/fixtures/json1.json'
JSON2 = 'tests/fixtures/json2.json'
YML1 = 'tests/fixtures/yml1.yml'
YML2 = 'tests/fixtures/yml2.yml'
BAD_JSON_EXT = 'tests/fixtures/json'
BAD_JSON_DATA = 'tests/fixtures/incorrect-json.json'
BAD_YML = 'tests/fixtures/yml.bak'
JSONDIFF1 = 'tests/fixtures/jsondiff1.txt'
EXPECTED_TEMP_DIFF = 'tests/fixtures/expected-json.json'
EXPECTED_STYLISH = 'tests/fixtures/expected-stylish.txt'
EXPECTED_PLAIN = 'tests/fixtures/expected-plain.txt'
FULL_JSON1 = 'tests/fixtures/full-json1.json'
FULL_JSON2 = 'tests/fixtures/full-json2.json'
FULL_YML1 = 'tests/fixtures/full-yml1.yml'
FULL_YML2 = 'tests/fixtures/full-yml2.yml'


def read(file_, as_json=False):
    with open(file_, 'r') as fixture:
        if as_json:
            return json.load(fixture)
        else:
            return fixture.read()


def test_json_load_errors():
    with pytest.raises(TypeError):
        load_file(BAD_JSON_EXT)
    with pytest.raises(ValueError):
        load_file(BAD_JSON_DATA)


def test_output():
    assert json.loads(read(EXPECTED_TEMP_DIFF)) == (
        json.loads(generate_diff(FULL_JSON1, FULL_JSON2, JSON_FORMAT))
    )
    assert json.loads(read(EXPECTED_TEMP_DIFF)) == (
        json.loads(generate_diff(FULL_YML1, FULL_YML2, JSON_FORMAT))
    )
    assert read(JSONDIFF1) == generate_diff(JSON1, JSON2, STYLISH_FORMAT)
    assert read(JSONDIFF1) == generate_diff(YML1, YML2, STYLISH_FORMAT)
    assert read(JSONDIFF1) == generate_diff(YML1, JSON2, STYLISH_FORMAT)
    assert read(EXPECTED_STYLISH) == generate_diff(
        FULL_JSON1, FULL_JSON2, STYLISH_FORMAT
    )
    assert read(EXPECTED_PLAIN) == generate_diff(
        FULL_JSON1, FULL_JSON2, PLAIN_FORMAT
    )
