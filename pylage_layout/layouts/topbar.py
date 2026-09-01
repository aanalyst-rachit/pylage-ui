"""Topbar layout composition."""

from typing import Any

from pylage import Navigation


def Topbar(*children, **props: Any):
    """Create a topbar using PyLage Navigation."""
    return Navigation(*children, **props)


__all__ = ["Topbar"]
