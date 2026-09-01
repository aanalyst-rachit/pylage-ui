"""High-level pagination layout composition for PyLage Layout."""

from typing import Any

from pylage.components import Pagination


def PaginationLayout(*children: Any, **props: Any):
    """Create a high-level pagination layout using PyLage Pagination."""
    return Pagination(*children, **props)
