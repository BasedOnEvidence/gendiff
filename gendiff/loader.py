import os

from gendiff.parser import parser
from gendiff.structures import formats


def get_data_from(file_path):
    extension = os.path.splitext(file_path)[-1]
    parser(extension)
    load_func, err = formats[extension]
    with open(file_path, 'r') as file_:
        try:
            return load_func(file_.read())
        except err:
            raise ValueError("Bad data in {}".format(file_path))
