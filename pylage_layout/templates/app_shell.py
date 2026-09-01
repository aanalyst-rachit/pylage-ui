"""Application shell page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import Column


def AppShell(
    content: Any,
    header: Any = None,
    sidebar: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a complete application shell from existing PyLage Layout pieces."""

    children = []

    if header is not None:
        children.append(header)

    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    body_children.append(content)

    body = Column(*body_children, class_name="app-shell-body")

    children.append(body)

    if footer is not None:
        children.append(footer)

    return Stack(*children, **props)
