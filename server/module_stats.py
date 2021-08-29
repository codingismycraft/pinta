"""Exposes a class that holds change statistics for all modules.

Using the git log we are creating a history of changes for each module
and also append to it the number of target dependencies.
"""

import csv

import change_history
import settings
import targets

# Aliases.
settings = settings.settings
Targets = targets.Targets


class ModuleStats:
    """Holds the statistics for a module.

    :ivar str _module_name: The name of the module
    :ivar list _affected_targets: The affected targets.
    :ivar int dependency_count: The number of dependencies.
    """

    def __init__(self, module_name, affected_targets, dependency_count,
                 change_rate, all_changes_count, latest_changes_count,
                 lifespan_in_days, filepath):
        """Initializer.

        :param str module_name: The module name.
        :param set affected_targets: The affected targets.
        """
        self._module_name = module_name
        self._affected_targets = list(affected_targets)
        self._dependency_count = dependency_count
        self._change_rate = change_rate
        self._all_changes_count = all_changes_count
        self._latest_changes_count = latest_changes_count
        self._lifespan_in_days = lifespan_in_days
        self._filepath = filepath

    @property
    def module_name(self):
        return self._module_name

    @property
    def affected_targets(self):
        return len(self._affected_targets)

    @property
    def dependency_count(self):
        return self._dependency_count

    @property
    def change_rate(self):
        return self._change_rate

    @property
    def all_changes_count(self):
        return self._all_changes_count

    @property
    def latest_changes_count(self):
        return self._latest_changes_count

    @property
    def lifespan_in_days(self):
        return self._lifespan_in_days

    @property
    def filepath(self):
        return self._filepath

    def __repr__(self):
        """Make debugging easier!"""
        return f'{self._module_name}, ' \
               f'Affected targets: {len(self._affected_targets)} ' \
               f'Dependencies: {self._dependency_count} ' \
               f'Change Rate: {self._change_rate} ' \
               f'Total Changes: {self._all_changes_count} ' \
               f'Latest Changes: {self._latest_changes_count} ' \
               f'Lifespan: {self._lifespan_in_days}'

    @classmethod
    def load_module_stats(cls):
        stats = []
        stats_per_module, dependency_counts = _module_stats()
        history = change_history.load_change_history()

        for module_name, affected_targets in stats_per_module.items():
            if module_name not in history:
                continue
            ch = history.get(module_name)
            lifespan_in_days = ch.lifespan_in_days if ch else 'n/a'
            change_rate = ch.change_rate if ch else 'n/a'
            all_changes_count = ch.changes_count if ch else 'n/a'
            latest_changes_count = ch.latest_changes_count if ch else 'n/a'
            filepath = ch.filepath if ch else 'n/a'

            stats.append(
                cls(
                    module_name=module_name,
                    affected_targets=affected_targets,
                    dependency_count=dependency_counts[module_name],
                    change_rate=change_rate,
                    all_changes_count=all_changes_count,
                    latest_changes_count=latest_changes_count,
                    lifespan_in_days=lifespan_in_days,
                    filepath=filepath

                )
            )
        return stats


def _module_stats():
    graph_from_target, graph_to_target = _create_graph()

    stats_per_module = {parent: set() for parent in graph_from_target.keys()}

    all_targets = Targets()
    for target in all_targets.get_all():
        _upadate_dependencies(
            graph_from_target,
            target.module_name,
            stats_per_module
        )

    dependency_counts = _count_dependencies(graph_to_target)
    return stats_per_module, dependency_counts


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
    graph_from_target = {}
    graph_to_target = {}

    with open(settings.dependencies_filename) as file:
        for tokens in csv.reader(file):
            n1 = tokens[0].strip()
            n2 = tokens[1].strip()

            if n1 not in graph_from_target:
                graph_from_target[n1] = []
            if n2 not in graph_from_target:
                graph_from_target[n2] = []
            graph_from_target[n2].append(n1)

            if n1 not in graph_to_target:
                graph_to_target[n1] = []
            if n2 not in graph_to_target:
                graph_to_target[n2] = []
            graph_to_target[n1].append(n2)

    return graph_from_target, graph_to_target


def _upadate_dependencies(graph, target, stats_per_module):
    stack = [(target, iter(graph[target]))]
    stats_per_module[target].add(target)
    visited = set()
    visited.add(target)
    while stack:
        parent, iter_to_children = stack[-1]
        stats_per_module[parent].add(target)
        try:
            child = next(iter_to_children)
            if child not in visited:
                stack.append((child, iter(graph[child])))
                visited.add(child)
        except StopIteration:
            stack.pop()


def _count_dependencies(graph):
    """Assigns the total number of dependencies to each node."""
    dependency_counter = {parent: 0 for parent in graph}
    for current_node in graph:
        stack = [[current_node, iter(graph[current_node])]]
        visited = set()
        visited.add(current_node)
        while stack:
            parent, children_iter = stack[-1]
            try:
                child = next(children_iter)
                if child not in visited:
                    visited.add(child)
                    dependency_counter[current_node] += 1
                    stack.append([child, iter(graph[child])])
            except StopIteration:
                stack.pop()
    return dependency_counter


def export_to_csv(filename):
    with open(filename, 'w') as file:
        tokens = [
            "name",
            "targets",
            "dependencies",
            "change-rate",
            "all-changes",
            "latest-changes",
            "lifespan-in-days"
        ]
        file.write(','.join(tokens))
        file.write("\n")

        for module in ModuleStats.load_module_stats():
            tokens = [
                module.module_name,
                module.affected_targets,
                module.dependency_count,
                module.change_rate,
                module.all_changes_count,
                module.latest_changes_count,
                module.lifespan_in_days
            ]
            file.write(','.join(str(t) for t in tokens))
            file.write("\n")


if __name__ == '__main__':
    export_to_csv("change_history.csv")
