"""Public application shell layout for PyLage Layout."""

from typing import Any

from pylage.components import Column, Row


def AppShell(
    *,
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    **props: Any,
):
    """Compose an application shell from header, sidebar, and content.

    Public Phase 8 API:

        AppShell(
            header=...,
            sidebar=...,
            content=...,
        )
    """
    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    if content is not None:
        body_children.append(content)

    body = Row(*body_children)

    children = []

    if header is not None:
        children.append(header)

    children.append(body)

    return Column(*children, **props)


__all__ = ["AppShell"]
