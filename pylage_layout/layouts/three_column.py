"""Three-column responsive layout for PyLage Layout."""

from typing import Any

from pylage import Row, Style, ResponsiveStyle


DEFAULT_THREE_COLUMN_STYLE = ResponsiveStyle(
    base=Style(
        display="flex",
        flex_direction="column",
        gap="1rem",
        width="100%",
    ),
    md=Style(
        flex_direction="row",
    ),
    lg=Style(
        gap="2rem",
    ),
)


def ThreeColumn(*children: Any, **props: Any):
    """Create a responsive three-column layout.

    Mobile:
        Columns stack vertically.

    Tablet/Desktop:
        Columns are arranged horizontally.
    """
    class_name = props.pop("class_name", "three-column")
    style = props.pop("style", None)

    if style is None:
        style = DEFAULT_THREE_COLUMN_STYLE

    return Row(
        *children,
        class_name=class_name,
        style=style,
        **props,
    )


__all__ = [
    "ThreeColumn",
    "DEFAULT_THREE_COLUMN_STYLE",
]
