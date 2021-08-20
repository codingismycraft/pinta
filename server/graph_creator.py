"""Creates the dependency list."""

import csv
import collections

import settings

# Aliases.
settings = settings.settings


GraphInfo = collections.namedtuple(
    "GraphInfo",
    [
        "nodes",
        "edges",
        "direct_dependencies"
    ]
)



def get_dependency_graph(node):
    """Returns the dependent nodes and the edges for the passed in node.

    :param str node: The node to get dependencies for.

    :return: A tuple consisting of the nodes and the edges.
    :rtype: tuple[list, list]
    """
    g = _make_graph()
    edges, direct_dependencies = _all_dependencies(node, g)

    all_nodes = set()
    for n1, n2 in edges:
        all_nodes.add(n1)
        all_nodes.add(n2)

    node_to_info = {}
    for index, node_name in enumerate(all_nodes):
        if node_name not in node_to_info:
            node_id = index + 1
            node_to_info[node_name] = {
                "id": node_id,
                "label": "",
                "title": node_name,
                "value": 1,
                "color": "blue"
            }

    node_to_info[node]['color'] = 'red'
    node_to_info[node]['value'] = 3


    edges_representation = []
    for n1, n2 in edges:
        index1 = node_to_info[n1]["id"]
        index2 = node_to_info[n2]["id"]

        edge_color = 'gray'
        value = 1
        if n1 == node:
            node_to_info[n2]['color'] = 'green'
            node_to_info[n2]['value'] = 2
            edge_color = 'green'
            value = 2

        if n2 == node:
            node_to_info[n1]['color'] = 'green'
            node_to_info[n1]['value'] = 2
            edge_color = 'green'
            value = 2

        edges_representation.append(
            {
                "from": index1,
                "to": index2,
                "color": edge_color,
                "value": value
            },
        )

    return list(node_to_info.values()), edges_representation, direct_dependencies


def _create_graph_from_edges(edges):
    """Creates a dependency graph from the passed in edges.

    :param list edges: A list of pairs from parent to child dependencies.

    :return: The edges as a dependency graph.
    :rtype: dict.
    """
    g = {}
    for n1, n2 in edges:
        n1 = n1.strip()
        n2 = n2.strip()
        if n1 not in g:
            g[n1] = []
        if n2 not in g:
            g[n2] = []
        g[n1].append(n2)
    return g


def _all_dependencies(node, dg):
    """Gets all the dependencies for the passed in node.

    :param str node: The node to lookup dependencies for.
    :param dict dg: The graph to lookup.

    :return: Tuple of a list of pairs from parent to child dependencies and
        the list of direct_dependencies.
    :rtype: list[tuple[str, str]], list
    """
    visited = set()
    queue = [node]
    edges = []
    direct_dependencies = []
    while queue:
        current_node = queue.pop(0)
        if current_node in visited:
            continue
        for child in dg[current_node]:
            assert child != current_node
            if child not in visited:
                edges.append((current_node, child))
                if current_node == node:
                    direct_dependencies.append(child)
                queue.append(child)
        visited.add(current_node)
    return edges, direct_dependencies


def _make_graph():
    """Creates the full graph of the code base.

    :return: The full graph of the code base.
    :rtype: dict.
    """
    g = {}
    filename = settings.dependencies_filename
    with open(filename, 'r') as f:
        for line_num, tokens in enumerate(csv.reader(f)):
            if line_num == 0:
                continue
            n1 = tokens[0].strip()
            n2 = tokens[1].strip()
            if n1 not in g:
                g[n1] = []
            if n2 not in g:
                g[n2] = []
            g[n1].append(n2)
    return g
