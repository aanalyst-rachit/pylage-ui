"""Reusable CTA pattern built from PyLage components."""

from typing import Any

from pylage.components import Button, Column, Heading, Row, Text


def CTA(
    title: Any,
    description: Any = None,
    actions: list[Any] | None = None,
    **props: Any,
):
    """Create a reusable call-to-action composition."""
    children = [
        Heading(title),
    ]

    if description is not None:
        children.append(Text(description))

    if actions:
        children.append(Row(*actions))

    return Column(
        *children,
        class_name=props.pop("class_name", "cta-section"),
        **props,
    )
