"""Exports reusable functions."""

import settings

# Aliases.
settings = settings.settings


def get_module_from_path(filepath):
    """Returns the corresponding python module to the passed in filepath.

    :param str filepath: The full path to the python file.

    :return: The corresponding python module to the passed in filepath.
    :rtype: str.
    """
    if not filepath.startswith('/'):
        filepath = '/' + filepath
    filepath = filepath.replace(settings.include_root, "")
    filepath = filepath.replace("/", ".")
    if filepath.startswith('.'):
        filepath = filepath[1:]
    if filepath.endswith('.py'):
        filepath = filepath[:-3]
    return filepath


def get_path_from_module(module):
    """Returns the corresponding path for the passed in python module.

    :param str module: The module to use.

    :return: The corresponding path for the passed in python module.
    :rtype: str.
    """
    filepath = module
    filepath = filepath.replace(".", "/")
    if not filepath.endswith(".py"):
        filepath += '.py'
    if not filepath.startswith("/"):
        filepath = '/' + filepath
    filepath = settings.include_root + filepath
    return filepath
