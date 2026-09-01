"""Center layout primitive for PyLage Layout."""

from typing import Any

from pylage import Column, Style


DEFAULT_CENTER_STYLE = Style(
    display="flex",
    justify_content="center",
    align_items="center",
    width="100%",
)


def Center(*children: Any, **props: Any):
    """Create a layout that centers its children."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_CENTER_STYLE

    return Column(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "Center",
    "DEFAULT_CENTER_STYLE",
]
