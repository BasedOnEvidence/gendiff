from gendiff import core


# Paths
JSON1 = "tests/fixtures/json1.json"
JSON2 = "tests/fixtures/json2.json"
JSONDIFF1 = "tests/fixtures/jsondiff1.txt"


def read(file_):
    with open(file_, "r") as input_file:
        answer = input_file.read()
    return answer


def tests():
    assert len(read(JSONDIFF1)) == len(core.generate_diff(JSON1, JSON2))
