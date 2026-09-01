"""Section layout primitive for PyLage Layout."""

from typing import Any

from pylage import Column, Style


DEFAULT_SECTION_STYLE = Style(
    width="100%",
    padding_top="4rem",
    padding_bottom="4rem",
)


def Section(*children: Any, **props: Any):
    """Create a full-width vertical page section."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_SECTION_STYLE

    return Column(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "Section",
    "DEFAULT_SECTION_STYLE",
]
