"""Creates the dependency list."""

import csv
import settings

import graph_info

# Aliases.
settings = settings.settings

def get_affected_tests(node):
    """Returns all the tests that are related to the passed in node.

    :param str node: The node to get dependencies for.
    """
    g = _make_graph()

    edges, direct_dependencies = _all_dependencies(node, g)
    affected_tests = set()

    if not edges:
        return affected_tests

    all_nodes = set()
    for n1, n2 in edges:
        all_nodes.add(n1)
        all_nodes.add(n2)

    for index, node_name in enumerate(all_nodes):
        filename = node_name.split('.')[-1]
        if filename.startswith("test_") or filename.endswith("_test"):
            affected_tests.add(node_name)

    return sorted(list(affected_tests))


def get_dependency_graph(node, targets=None):
    """Returns the dependent nodes and the edges for the passed in node.

    :param str node: The node to get dependencies for.
    :param list targets: A list with the modules that are used as targets.

    :return: The dependency graph info.
    :rtype: GraphInfo
    """
    g = _make_graph()

    edges, direct_dependencies = _all_dependencies(node, g)

    if targets:
        targets = set(targets)

    affected_targets = []

    if not edges:
        return graph_info.GraphInfo(
            graph=g,
            nodes=[],
            edges=[],
            direct_dependencies=[],
            affected_targets=[]
        )

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
            if targets and node_name in targets:
                node_to_info[node_name]["color"] = 'orange'
                node_to_info[node_name]["value"] = 3
                affected_targets.append(node_name)

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

    info = graph_info.GraphInfo(
        graph=g,
        nodes=list(node_to_info.values()),
        edges=edges_representation,
        direct_dependencies=sorted(direct_dependencies),
        affected_targets=affected_targets
    )
    return info


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
        visited.add(current_node)
        for child in dg[current_node]:
            if child not in visited:
                assert child != current_node
                edges.append((current_node, child))
                if current_node == node:
                    direct_dependencies.append(child)
                queue.append(child)

    return edges, direct_dependencies


def _make_graph():
    """Creates the full graph of the code base.

    :return: The full graph of the code base.
    :rtype: dict.
    """
    graph = {}
    filename = settings.dependencies_filename
    with open(filename, 'r') as f:
        for line_num, tokens in enumerate(csv.reader(f)):
            if line_num == 0:
                continue
            n1 = tokens[0].strip()
            n2 = tokens[1].strip()
            if n1 not in graph:
                graph[n1] = []
            if n2 not in graph:
                graph[n2] = []
            graph[n1].append(n2)
    return graph
