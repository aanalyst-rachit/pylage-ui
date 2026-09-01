"""Header layout primitive for PyLage Layout."""

from typing import Any

from pylage.core.component import component


def Header(*children, **props: Any):
    return component("Header", *children, **props)


__all__ = ["Header"]
