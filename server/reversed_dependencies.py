"""Represents the reversed DAG as an adjacency list matrix."""

import csv


class ReverseDependencies:
    """Represents the reversed DAG as an adjacency list matrix.

    :ivar dict _graph: Holds the graph.
    """

    _graph = None

    def __init__(self, filename):
        """Initializer.

        :param str filename: The filename that contains the dependencies.
        """
        self._graph = {}
        with open(filename, 'r') as f:
            for tokens in csv.reader(f):
                n1 = tokens[0].strip()
                n2 = tokens[1].strip()

                if n1 not in self._graph:
                    self._graph[n1] = []

                if n2 not in self._graph:
                    self._graph[n2] = []

                self._graph[n2].append(n1)

    def count_reversed_dependencies(self, node):
        """Counts the reversed dependencies of the passed in node.

        :param str node: The node name to use.

        :returns: The number of reversed dependencies of the passed in node
        :rtype: int.
        """
        node = node.strip()
        if node not in self._graph:
            return 0
        queue = [node]
        visited = set()
        count = 0
        while queue:
            current_node = queue.pop(0)
            if current_node in visited:
                continue
            count += 1
            for child in self._graph[current_node]:
                if child not in visited:
                    queue.append(child)

            visited.add(current_node)
        return count
