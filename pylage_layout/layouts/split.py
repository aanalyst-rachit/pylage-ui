"""Split layout primitive for PyLage Layout."""

from typing import Any

from pylage import Row, Style, ResponsiveStyle


DEFAULT_SPLIT_STYLE = ResponsiveStyle(
    base=Style(
        display="flex",
        width="100%",
        flex_direction="column",
        gap="1rem",
    ),
    md=Style(
        flex_direction="row",
    ),
    lg=Style(
        gap="2rem",
    ),
)


def Split(*children: Any, **props: Any):
    """Create a responsive split layout."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_SPLIT_STYLE

    return Row(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "Split",
    "DEFAULT_SPLIT_STYLE",
]
