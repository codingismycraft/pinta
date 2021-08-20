"""Exposes the configuration settings."""

import os
import json


class _Settings:
    """Exposes the configuration settings."""

    _project_root = None
    _include_root = None
    _dependencies_filename = None

    def __init__(self):
        """Initializer.

        Loads the settings using the pinta configuration file.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, "..", "pinta", "depender.json")
        with open(filename) as json_file:
            data = json.load(json_file)
            self._project_root = data["project_root"]
            self._include_root = data["include_root"]
            self._dependencies_filename = data["dependencies_filename"]

    @property
    def project_root(self):
        """Returns the project root.

        :return: The project root.
        :rtype: str.
        """
        return self._project_root

    @property
    def include_root(self):
        """Returns the include root for all python imports.

       :return: The include root.
       :rtype: str.
       """
        return self._include_root

    @property
    def dependencies_filename(self):
        """Returns the filename that containg the dependencies as csv.

        :return: The filename that containg the dependencies as csv.
        :rtype: str.
        """
        return self._dependencies_filename


settings = _Settings()
