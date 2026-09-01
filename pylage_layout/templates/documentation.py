"""Documentation page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import (
    Row,
    Column,
    Card,
    Heading,
    Text,
    Button,
    Icon,
    Input,
    Tabs,
    Table,
    Badge,
)


def Documentation(
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a complete documentation page."""

    children = []

    if header is not None:
        children.append(header)

    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    if content is not None:
        body_children.append(content)

    if body_children:
        children.append(Row(*body_children, class_name="docs-body"))

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(*children, **props)
    )
