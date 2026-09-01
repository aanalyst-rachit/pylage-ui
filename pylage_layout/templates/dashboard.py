"""Dashboard page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import Column, Row


def Dashboard(
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    stats: Any = None,
    table: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a dashboard page from existing PyLage Layout primitives."""

    children = []

    if header is not None:
        children.append(header)

    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    main_children = []

    if stats is not None:
        main_children.append(stats)

    if content is not None:
        main_children.append(content)

    if table is not None:
        main_children.append(table)

    main = Column(
        *main_children,
        class_name="dashboard-main",
    )

    body_children.append(main)

    body = Row(
        *body_children,
        class_name="dashboard-body",
    )

    children.append(body)

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(*children, **props)
    )
