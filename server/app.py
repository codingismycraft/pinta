import json

from flask import Flask
from flask import render_template

import graph_creator
import settings

# Aliases.
settings = settings.settings

app = Flask(__name__)


def _get_module_from_path(filepath):
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
    varargs = varargs.split("/")
    filepath = '/'.join(varargs)
    module_name = _get_module_from_path(filepath)
    nodes_to_use, edges_to_use = graph_creator.get_dependency_graph(module_name)
    # nodes_to_use = [
    #     {"id": 1, "label": "", "title": "I have a popup1!", "color": "red"},
    #     {"id": 2, "label": "", "title": "I have a popup2!"},
    #     {"id": 3, "label": "", "title": "I have a popup3!"},
    #     {"id": 4, "label": "", "title": "I have a popup4!"},
    #     {"id": 5, "label": "", "title": "I have a popup5!"}
    # ]
    #
    # edges_to_use = [
    #     {"from": 1, "to": 3},
    #     {"from": 1, "to": 2},
    #     {"from": 1, "to": 5},
    #     {"from": 2, "to": 4},
    #     {"from": 2, "to": 5},
    #     {"from": 4, "to": 5}
    # ]

    return render_template(
        'show_graph.html',
        filepath=module_name,
        nodes_to_use=json.dumps(nodes_to_use),
        edges_to_use=json.dumps(edges_to_use)
    )


if __name__ == '__main__':
    app.run()
