"""Simple server to display code dependencies."""

import json

from flask import Flask
from flask import render_template

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


@app.route("/<path:varargs>")
def data(varargs=None):
    """Returns a webpage with the dependencies for the requested file."""
    varargs = varargs.split("/")
    filepath = '/'.join(varargs)
    module_name = _get_module_from_path(filepath)
    nodes_to_use, edges_to_use, direct_dependencies = graph_creator.get_dependency_graph(
        module_name)

    number_of_nodes = len(nodes_to_use)
    number_of_edges = len(edges_to_use)

    doc_title = module_name
    if '.' in doc_title:
        doc_title = doc_title.split('.')[-1]

    direct_dependencies = [
        (dd, _get_path_from_module(dd))
        for dd in direct_dependencies
    ]

    return render_template(
        'show_graph.html',
        doc_title=doc_title,
        filepath=module_name,
        nodes_to_use=json.dumps(nodes_to_use),
        edges_to_use=json.dumps(edges_to_use),
        number_of_nodes=number_of_nodes,
        number_of_edges=number_of_edges,
        direct_dependencies_count=len(direct_dependencies),
        direct_dependencies=direct_dependencies
    )


if __name__ == '__main__':
    # print(_get_path_from_module("pants.services.data.borrelly.impl.aggregatorpool"))
    app.run()
