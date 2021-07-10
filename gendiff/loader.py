import os

from gendiff.parser import parser


def get_data_from(file_path):
    extension = os.path.splitext(file_path)[-1][1:]
    with open(file_path, 'r') as file_:
        try:
            return parser(file_.read(), extension)
        except ValueError as err:
            raise ValueError('Bad data in {}'.format(file_path)) from err
