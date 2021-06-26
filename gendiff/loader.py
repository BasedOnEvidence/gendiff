import os

from gendiff.parser import parser


def load_file(file_path):
    extension = os.path.splitext(file_path)[1]
    with open(file_path, 'r') as file_:
        return parser(file_.read(), extension, file_path)
