"""Admin panel page template for PyLage Layout."""

from typing import Any

from pylage.components import (
    Badge,
    Button,
    Card,
    Column,
    Heading,
    Icon,
    Pagination,
    Row,
    Table,
    Tabs,
    Text,
)


def AdminPanel(
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose an admin panel from reusable PyLage components."""

    children = []

    if header is not None:
        children.append(header)

    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    if content is not None:
        body_children.append(content)

    body = Row(
        *body_children,
        class_name="admin-panel-body",
    )

    children.append(body)

    if footer is not None:
        children.append(footer)

    return Column(
        *children,
        class_name="admin-panel",
        **props,
    )
