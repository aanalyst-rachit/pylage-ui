"""Menu/dropdown layout for PyLage Layout."""

from typing import Any

from pylage import components


def _component(name: str, *children: Any, **props: Any):
    factory = getattr(components, name, None)
    if factory is None:
        raise RuntimeError(f"PyLage component {name!r} is not available")
    return factory(*children, **props)


def MenuLayout(*children: Any, **props: Any):
    """Create a menu layout using PyLage's Menu primitive."""
    return _component("Menu", *children, **props)


def SelectLayout(*children: Any, **props: Any):
    """Create a select/dropdown-style layout using PyLage's Select primitive."""
    return _component("Select", *children, **props)


__all__ = ["MenuLayout", "SelectLayout"]
