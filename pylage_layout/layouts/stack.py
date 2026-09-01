"""Stack layout primitive for PyLage Layout."""

from typing import Any

from pylage import Column, Style, ResponsiveStyle


DEFAULT_STACK_STYLE = ResponsiveStyle(
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


def Stack(*children: Any, **props: Any):
    """Create a responsive stack layout."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_STACK_STYLE

    return Column(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "Stack",
    "DEFAULT_STACK_STYLE",
]
