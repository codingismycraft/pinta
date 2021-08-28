"""Exposes class to summarize the data that will be passed to the webpage."""


class GraphInfo:
    """Summarizes the data that will be passed to the webpage.

    :ivar list _nodes: All the affected nodes.
    :ivar list _edges: All the affected edges.
    :ivar list _direct_dependencies: The direct dependencies.
    :ivar list _affected_targets: The affected targets.
    :ivar list _graph_stats: The counts of all nodes and edges in the graph.
    :ivar list _disconnected_subgraphs: The _disconnected_subgraphs.
    """
    _nodes = None
    _edges = None
    _direct_dependencies = None
    _affected_targets = None
    _graph_stats = None
    _disconnected_subgraphs = None

    def __init__(self, graph, nodes=None, edges=None, direct_dependencies=None,
                 affected_targets=None):
        """Initializer."""
        self._nodes = nodes or []
        self._edges = edges or []
        self._direct_dependencies = direct_dependencies or []
        self._affected_targets = affected_targets or []
        self._graph_stats = self._make_graph_stats(graph)
        self._disconnected_subgraphs = self._get_disconnected_subgraphs(graph)

    @property
    def nodes(self):
        """Returns the dependant nodes."""
        return self._nodes

    @property
    def edges(self):
        """Returns the dependant edges."""
        return self._edges

    @property
    def direct_dependencies(self):
        """Returns the direct dependencies."""
        return self._direct_dependencies

    @property
    def affected_targets(self):
        """Returns the affected_targets."""
        return self._affected_targets

    @property
    def graph_stats(self):
        """Returns the (full graph) stats."""
        return self._graph_stats

    @property
    def disconnected_subgraphs(self):
        """Returns the disconnected_subgraphs."""
        return self._disconnected_subgraphs

    @classmethod
    def _make_graph_stats(cls, graph):
        """Returns statistics for the passed in graph.

        :param dict graph: The graph to get statistics for.

        :return: The statistics for the passed in graph.
        :rtype: list[tuple].
        """
        edge_count = 0

        for edges in graph.values():
            edge_count += len(edges)

        return [
            ("Nodes", f'{len(graph):,}'),
            ("Edges", f'{edge_count:,}'),
        ]

    def _get_disconnected_subgraphs(self, graph):
        """Returns the the disconnected subgraphs.

        :param dict graph: The graph to search for subgraphs.

        :return: List of tuples holding the nodes count and indicative_module
        for each subgraph.

        :rtype: list[Tuple[int, str]].
        """
        subgraphs = self._find_disconnected_graphs(graph)
        indicative_modules = []
        for subgraph in subgraphs:
            indicative_module = None
            counter = -1
            for key, values in subgraph.items():
                if counter < len(values):
                    indicative_module = key
                    counter = len(values)
            indicative_modules.append((len(subgraph), indicative_module))
        return indicative_modules

    def _find_disconnected_graphs(self, graph):
        """Finds all the "weakly" disconnected sub-graphs of a graph.

        :param dict graph: The graph to search.

        :returns: A list of the disconnected sub-graphs.
        :rtype: list[dict]
        """
        graph = self._make_weakly_connected_graph(graph)
        graphs = []
        nodes = list(graph.keys())
        while nodes:
            node = nodes.pop()
            graphs.append(self._get_connected_subgraph(graph, node, nodes))
        return graphs

    @classmethod
    def _make_weakly_connected_graph(cls, graph):
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

    @classmethod
    def _get_connected_subgraph(cls, graph, node_to_start_from, nodes):
        """Finds the connected sub-graph for the passed node.

        :param dict graph: The graph to search.
        :param str node_to_start_from: The node to search.

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
                if child not in visited:
                    subgraph[current_node].append(child)
                    queue.append(child)

        visited.remove(node_to_start_from)
        for node in visited:
            nodes.remove(node)

        return subgraph
