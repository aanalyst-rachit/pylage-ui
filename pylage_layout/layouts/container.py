"""Container layout primitive for PyLage Layout."""

from typing import Any

from pylage import Column, Style, ResponsiveStyle


DEFAULT_CONTAINER_STYLE = ResponsiveStyle(
    base=Style(
        width="100%",
        flex_direction="column",
        max_width="1200px",
        margin="0 auto",
    ),
    md=Style(
        flex_direction="row",
    ),
    lg=Style(
        gap="2rem",
    ),
)


def Container(*children: Any, **props: Any):
    """Create a centered, width-constrained responsive page container."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_CONTAINER_STYLE

    return Column(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "Container",
    "DEFAULT_CONTAINER_STYLE",
]
