import os
import string

import termcolor


def get_template(template_file_path, color=None):
    template = find_template(template_file_path)
    with open(template, 'r', encoding='utf-8') as template_file:
        contents = template_file.read()
        contents = contents.rstrip(os.linesep)
        contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(contents=contents, splitter='=' * 60, sep=os.linesep)
        contents = termcolor.colored(contents, color)
        return string.Template(contents)


class NoTemplateError(Exception):
    """ NO Template Error """


def find_template(temp_file):
    temp_dir_path = get_template_dir_path()
    temp_file_path = os.path.join(temp_dir_path, temp_file)

    if not os.path.exists(temp_file_path):
        raise NoTemplateError('Could not find {}'.formart(temp_file))

    return temp_file_path


def get_template_dir_path():
    template_dir_path = None
    try:
        import settings
        if settings.TEMPLATE_PATH:
            template_dir_path = settings.TEMPLATE_PATH
    except ImportError:
        pass

    if not template_dir_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir_path = os.path.join(base_dir, 'templates')

    return template_dir_path
