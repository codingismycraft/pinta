"""Finds all the disconnected sub-graphs of a graph."""


def find_disconnected_graphs(graph):
    """Finds all the "weakly" disconnected sub-graphs of a graph.

    :param dict graph: The graph to search.

    :returns: A list of the disconnected sub-graphs.
    :rtype: list[dict]
    """
    graph = _make_weakly_connected_graph(graph)
    graphs = []
    nodes = list(graph.keys())
    while nodes:
        node = nodes.pop()
        graphs.append(_get_connected_subgraph(graph, node, nodes))
    return graphs


def _make_weakly_connected_graph(graph):
    """Assures that the graph is weakly connected.

    :param dict graph: The graph to assure weak connectivity.

    :returns: The weakly connected graph.
    :rtype: dict.
    """
    weak_graph = {}

    for k, v in graph.items():
        weak_graph[k] = set(v)

    for node1, children in weak_graph.copy().items():
        for node2 in children:
            if node2 not in weak_graph:
                weak_graph[node2] = set()
            if node1 not in weak_graph[node2]:
                weak_graph[node2].add(node1)

    return weak_graph


def _get_connected_subgraph(graph, node_to_start_from, nodes):
    """Finds the connected sub-graph for the passed node.

    :param dict graph: The graph to search.
    :param str node: The node to find the connected subgraph.

    :returns: The connected sub-graph for the passed node.
    """
    assert node_to_start_from in graph

    subgraph = {}
    queue = [node_to_start_from]
    visited = set()

    while queue:
        current_node = queue.pop(0)

        if current_node in visited:
            continue

        if current_node not in subgraph:
            subgraph[current_node] = []

        visited.add(current_node)

        for child in graph[current_node]:
            if child in visited:
                continue
            subgraph[current_node].append(child)
            queue.append(child)

    visited.remove(node_to_start_from)
    for node in visited:
        if node not in nodes:
            junk = 1
        nodes.remove(node)

    return subgraph
