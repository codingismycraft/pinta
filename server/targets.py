"""Simple server to display code dependencies."""

import os
import settings
import reversed_dependencies

# Aliases.
settings = settings.settings
ReverseDependencies = reversed_dependencies.ReverseDependencies


class Target:
    """Holds the reversed dependencies for a module.

    :ivar str _filename: The full path to the target.
    :ivar int _reversed_dependencies_count: The "reversed_dependencies" count.
    """

    def __init__(self, rd, filename):
        """Initializer.

        :param ReverseDependencies rd: The reverse dependency graph.
        :param str filename The full path to the target:
        """
        self._filename = filename.strip()
        self._reversed_dependencies_count = rd.count_reversed_dependencies(
            self.module_name
        )

    @property
    def target_name(self):
        """Returns the target_name.

        :return: The target name.
        :rtype: str.
        """
        tokens = self.module_name.split('.')
        return tokens[-1].replace("_target", "")

    @property
    def module_name(self):
        """Returns the module name.

        :returns: The module name.
        :rtype: str.
        """
        return self._get_module_from_path(self._filename)

    @property
    def reversed_dependencies_count(self):
        """Returns the module name.

        :returns: The reversed dependencies count.
        :rtype: int.
        """
        return self._reversed_dependencies_count

    @property
    def filename(self):
        """Returns the full path to the file containing the target.

        :returns: The full path to the file containing the target.
        :rtype: str.
        """
        return self._filename

    def _get_module_from_path(self, filepath):
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

    def __repr__(self):
        """Make debugging easier!"""
        return f'Target: {self.target_name}' \
               f' ({self._reversed_dependencies_count})'


def get_all_targets():
    """Returns all the targets sorted by reversed_dependency count.

    :return: A list of Target instances.
    :rtype: list[Target]
    """
    rd = ReverseDependencies(settings.dependencies_filename)
    cmd = f'find {settings.project_root} -type f -iname "*target*py" > tmp'
    os.system(cmd)
    lines = open('tmp', 'r').readlines()
    os.remove("tmp")
    targets = [Target(rd, filename=line) for line in lines]
    return sorted(
        targets,
        key=lambda x: x.reversed_dependencies_count, reverse=True
    )
