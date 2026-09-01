"""Navigation layout for PyLage Layout."""

from pylage import Navigation as _Navigation


def Navigation(*children, **props):
    """Create a PyLage Navigation component."""
    return _Navigation(*children, **props)


__all__ = ["Navigation"]
