"""Navbar layout composition for PyLage Layout."""

from typing import Any

import pylage as ps


def Navbar(*children, **props: Any):
    """Create a high-level navigation bar using PyLage Navigation."""
    return ps.Navigation(
        *children,
        class_name=props.pop("class_name", "navbar"),
        **props,
    )


__all__ = ["Navbar"]
