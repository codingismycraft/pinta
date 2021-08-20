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


@app.route("/<path:varargs>")
def data(varargs=None):
    """Returns a webpage with the dependencies for the requested file."""
    varargs = varargs.split("/")
    filepath = '/'.join(varargs)
    module_name = _get_module_from_path(filepath)
    nodes_to_use, edges_to_use = graph_creator.get_dependency_graph(module_name)

    return render_template(
        'show_graph.html',
        filepath=module_name,
        nodes_to_use=json.dumps(nodes_to_use),
        edges_to_use=json.dumps(edges_to_use)
    )


if __name__ == '__main__':
    app.run()
