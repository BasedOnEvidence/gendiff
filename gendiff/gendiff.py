from gendiff.analyser import generate_temp_diff
from gendiff.output import output_selector


def generate_diff(
    first_file, second_file,
    style=output_selector.DEFAULT_FORMAT
):
    temp_diff = generate_temp_diff(first_file, second_file)
    diff = output_selector.gen_output(temp_diff, style)
    return diff
