"""Exposes a class that holds the change history for all modules.

Using the git log we are creating a history of changes for each module
and also append to it the number of target dependencies.
"""

import csv

import settings
import targets

# Aliases.
settings = settings.settings
Targets = targets.Targets


class ModuleStats:
    """Holds the statistics for a module.

    :ivar str _module_name: The name of the module
    :ivar list _affected_targets: The affected targets.
    """

    def __init__(self, module_name, affected_targets):
        """Initializer.

        :param str module_name: The module name.
        :param set affected_targets: The affected targets.
        """
        self._module_name = module_name
        self._affected_targets = list(affected_targets)

    def __repr__(self):
        """Make debugging easier!"""
        return f'ModuleStats: {self._module_name}, ' \
               f'{len(self._affected_targets)}'

    @classmethod
    def load_module_stats(cls):
        return [
            cls(module_name=module_name, affected_targets=affected_targets)
            for module_name, affected_targets in _target_dependencies().items()
        ]


def _target_dependencies():
    graph = _create_graph()
    dependencies = {
        parent: set()
        for parent in graph.keys()
    }
    all_targets = Targets()
    for target in all_targets.get_all():
        _upadate_dependencies(graph, target.module_name, dependencies)

    return dependencies


def _create_graph():
    """Creates the reversed dependencies graph.

    The adjacent edges as the are recorded in the dependencies file represent
    an "out" relationship between the imported and the importing modules.

    Here we need the reversed dependency meaning the "in" dependency because
    the goal is to discover how each module affects each of the targets. This
    why we are constructing the graph in the opposite direction meaning from
    the second to the first node as it appears in the dependency file.

    :return: The "in" dependency graph for the dependencies file.
    :rtype: dict
    """
    graph = {}

    with open(settings.dependencies_filename) as file:
        for tokens in csv.reader(file):
            n1 = tokens[0].strip()
            n2 = tokens[1].strip()
            if n1 not in graph:
                graph[n1] = []
            if n2 not in graph:
                graph[n2] = []
            graph[n2].append(n1)

    return graph


def _upadate_dependencies(graph, target, dependencies):
    stack = [(target, iter(graph[target]))]
    dependencies[target].add(target)
    visited = set()
    visited.add(target)
    while stack:
        parent, iter_to_children = stack[-1]
        dependencies[parent].add(target)
        try:
            child = next(iter_to_children)
            if child not in visited:
                stack.append((child, iter(graph[child])))
                visited.add(child)
        except StopIteration:
            stack.pop()


if __name__ == '__main__':

    for module in ModuleStats.load_module_stats():
        print(module)
