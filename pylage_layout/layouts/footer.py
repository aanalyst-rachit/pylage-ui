"""Footer layout primitive for PyLage Layout."""

from typing import Any

from pylage.core.component import component


def Footer(*children, **props: Any):
    return component("Footer", *children, **props)


__all__ = ["Footer"]
