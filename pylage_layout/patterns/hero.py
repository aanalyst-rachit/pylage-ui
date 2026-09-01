"""Reusable Hero pattern built on top of PyLage components."""

from typing import Any

from pylage.components import Button, Column, Heading, Row, Text


def Hero(
    title: Any,
    description: Any = None,
    actions: list[Any] | tuple[Any, ...] | None = None,
    **props: Any,
):
    """Create a reusable hero section from existing PyLage components."""

    children = [
        Heading(title),
    ]

    if description is not None:
        children.append(Text(description))

    if actions:
        action_components = []

        for action in actions:
            if isinstance(action, str):
                action_components.append(Button(action))
            else:
                action_components.append(action)

        children.append(Row(*action_components))

    return Column(*children, **props)
