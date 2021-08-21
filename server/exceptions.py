"""Exposes the custom exceptions used."""


class PintaServerException(Exception):
    """Generic pinta exception."""


class NoDependenciesFound(PintaServerException):
    """No dependencies found."""
