"""Reusable content section pattern built on PyLage components."""

from typing import Any

from pylage.components import Button, Card, Column, Heading, Image, Row, Text


def ContentSection(
    title: Any,
    content: Any = None,
    *,
    image: Any = None,
    actions: list[Any] | None = None,
    class_name: str = "content-section",
    **props: Any,
):
    """Create a reusable content section using existing PyLage components."""

    children = [
        Heading(title),
    ]

    if content is not None:
        children.append(Text(content))

    if image is not None:
        if isinstance(image, str):
            children.append(Image(src=image, alt=""))
        else:
            children.append(image)

    if actions:
        children.append(Row(*actions))

    return Column(
        *children,
        class_name=class_name,
        **props,
    )
