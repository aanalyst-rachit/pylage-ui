"""Navigation controls for PyLage Layout."""

from pylage.core.component import component


def Pagination(*children, **props):
    return component("Pagination", *children, **props)


def Menu(*children, **props):
    return component("Menu", *children, **props)


__all__ = ["Pagination", "Menu"]
