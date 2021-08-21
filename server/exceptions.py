"""Exposes the custom exceptions used."""


class PintaServerException(Exception):
    """Generic pinta exception."""


class NoDependenciesFound(PintaServerException):
    """No dependencies found."""


class TargetNotFound(PintaServerException):
    """Target not found."""
