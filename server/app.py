"""Simple server to display code dependencies."""

import os
import json

from flask import Flask
from flask import render_template

import exceptions
import graph_creator
import settings

# Aliases.
settings = settings.settings

app = Flask(__name__)


def _get_module_from_path(filepath):
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


def _get_path_from_module(module):
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


def _get_targets():
    cmd = f'find {settings.project_root} -type f -iname "*target*py" > tmp'
    os.system(cmd)
    lines = open('tmp', 'r').readlines()
    os.remove("tmp")
    return [_get_module_from_path(line.strip()) for line in lines]


def _abbreviate_module_name(module_name):
    """Abbreviates the passed in module_name.

    :param str module_name: The full module_name to abbreviate.

    :return: The abbreviated module name.
    :rtype: str.
    """
    tokens = module_name.split('.')
    return tokens[-1]


def _get_target_name(module_name):
    """Returns the target_name.

    :param str module_name: The full module_name of the target.


    :return: The target name.
    :rtype: str.
    """
    tokens = module_name.split('.')
    return tokens[-1].replace("_target", "")


@app.route("/<path:varargs>")
def data(varargs=None):
    """Returns a webpage with the dependencies for the requested file."""
    varargs = varargs.split("/")

    filepath = '/'.join(varargs)
    module_name = _get_module_from_path(filepath)
    try:
        nodes_to_use, edges_to_use, direct_dependencies, affected_targets = \
            graph_creator.get_dependency_graph(module_name, _get_targets())
    except exceptions.NoDependenciesFound:
        nodes_to_use = []
        edges_to_use = []
        direct_dependencies = []
        affected_targets = []

    number_of_nodes = len(nodes_to_use)
    number_of_edges = len(edges_to_use)

    doc_title = module_name
    if '.' in doc_title:
        doc_title = doc_title.split('.')[-1]

    direct_dependencies = [
        (_abbreviate_module_name(dd), _get_path_from_module(dd))
        for dd in direct_dependencies
    ]

    affected_targets = [
        (_get_target_name(trgt), _get_path_from_module(trgt))
        for trgt in affected_targets
    ]

    affected_targets.sort(key=lambda trgt: trgt[0])
    direct_dependencies.sort(key=lambda trgt: trgt[0])

    return render_template(
        'show_graph.html',
        doc_title=doc_title,
        filepath=module_name,
        nodes_to_use=json.dumps(nodes_to_use),
        edges_to_use=json.dumps(edges_to_use),
        number_of_nodes=number_of_nodes,
        number_of_edges=number_of_edges,
        direct_dependencies_count=len(direct_dependencies),
        direct_dependencies=direct_dependencies,
        affected_targets_count=len(affected_targets),
        affected_targets=affected_targets
    )


if __name__ == '__main__':
    # print(_get_path_from_module("pants.services.data.borrelly.impl.aggregatorpool"))
    app.run()
