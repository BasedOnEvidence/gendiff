from gendiff import core


# Paths
JSON1 = "tests/fixtures/json1.json"
JSON2 = "tests/fixtures/json2.json"
YML1 = "tests/fixtures/yml1.yml"
YML2 = "tests/fixtures/yml2.yml"
BAD_JSON = "tests/fixtures/json"
BAD_YML = "tests/fixtures/yml.bak"
JSONDIFF1 = "tests/fixtures/jsondiff1.txt"


def read(file_):
    with open(file_, "r") as input_file:
        answer = input_file.read()
    return answer


def tests():
    assert len(read(JSONDIFF1)) == len(core.generate_diff(JSON1, JSON2))
    assert len(read(JSONDIFF1)) == len(core.generate_diff(YML1, YML2))
    assert len(read(JSONDIFF1)) == len(core.generate_diff(YML1, JSON2))
    assert "{\n}" == core.generate_diff(BAD_YML, BAD_JSON)
