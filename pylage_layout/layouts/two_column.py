"""Two-column layout primitive for PyLage Layout."""

from typing import Any

from pylage import Row, Style, ResponsiveStyle


DEFAULT_TWO_COLUMN_STYLE = ResponsiveStyle(
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


def TwoColumn(*children: Any, **props: Any):
    """Create a responsive two-column layout."""
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_TWO_COLUMN_STYLE

    return Row(
        *children,
        style=style,
        **props,
    )


__all__ = [
    "TwoColumn",
    "DEFAULT_TWO_COLUMN_STYLE",
]
