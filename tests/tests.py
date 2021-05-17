from gendiff.constants import (
    STYLISH_FORMAT, PLAIN_FORMAT, JSON_FORMAT
)
from gendiff.gendiff import generate_diff


# Paths
JSON1 = "tests/fixtures/json1.json"
JSON2 = "tests/fixtures/json2.json"
YML1 = "tests/fixtures/yml1.yml"
YML2 = "tests/fixtures/yml2.yml"
BAD_JSON = "tests/fixtures/json"
BAD_YML = "tests/fixtures/yml.bak"
JSONDIFF1 = "tests/fixtures/jsondiff1.txt"
EXPECTED_TEMP_DIFF = "tests/fixtures/expected-json.json"
EXPECTED_STYLISH = "tests/fixtures/expected-stylish.txt"
EXPECTED_PLAIN = "tests/fixtures/expected-plain.txt"
FULL_JSON1 = "tests/fixtures/full-json1.json"
FULL_JSON2 = "tests/fixtures/full-json2.json"
FULL_YML1 = "tests/fixtures/full-yml1.yml"
FULL_YML2 = "tests/fixtures/full-yml2.yml"


def read(file_):
    with open(file_, "r") as input_file:
        answer = input_file.read()
    return answer


def tests():
    assert read(EXPECTED_TEMP_DIFF) == (
        generate_diff(FULL_JSON1, FULL_JSON2, JSON_FORMAT)
    )
    assert read(EXPECTED_TEMP_DIFF) == (
        generate_diff(FULL_YML1, FULL_YML2, JSON_FORMAT)
    )
    assert read(JSONDIFF1) == generate_diff(JSON1, JSON2, STYLISH_FORMAT)
    assert read(JSONDIFF1) == generate_diff(YML1, YML2, STYLISH_FORMAT)
    assert read(JSONDIFF1) == generate_diff(YML1, JSON2, STYLISH_FORMAT)
    assert "{\n}" == generate_diff(BAD_YML, BAD_JSON, STYLISH_FORMAT)
    assert read(EXPECTED_STYLISH) == (
        generate_diff(FULL_JSON1, FULL_JSON2, STYLISH_FORMAT)
    )
    print(read(EXPECTED_STYLISH))
    assert read(EXPECTED_PLAIN) == (
        generate_diff(FULL_JSON1, FULL_JSON2, PLAIN_FORMAT)
    )


def main():
    tests()


if __name__ == "__main__":
    main()
