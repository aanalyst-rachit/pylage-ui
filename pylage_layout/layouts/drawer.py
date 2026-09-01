"""Responsive drawer layout for PyLage Layout."""

from typing import Any

from pylage.components import Drawer


def NavigationDrawer(*children: Any, **props: Any):
    """Create a navigation drawer using PyLage's Drawer component."""
    return Drawer(*children, **props)


def MobileSidebar(*children: Any, **props: Any):
    """Create a mobile sidebar using PyLage's Drawer component."""
    return Drawer(*children, **props)


__all__ = [
    "NavigationDrawer",
    "MobileSidebar",
]
