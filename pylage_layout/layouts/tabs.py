"""High-level tab layout composition for PyLage Layout."""

from typing import Any

from pylage.components import Tabs


def TabLayout(*children: Any, **props: Any):
    """Create a high-level tab layout using PyLage Tabs."""
    return Tabs(*children, **props)
