from gendiff.structures import formats


def parser(extension):
    if extension not in formats.keys():
        raise TypeError(
            "File have to be one of the folowing formats: {}".format(
                formats.keys()
            )
        )
