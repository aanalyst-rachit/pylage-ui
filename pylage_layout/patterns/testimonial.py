"""Reusable testimonial pattern for PyLage Layout."""

from typing import Any

from pylage.components import Avatar, Card, Column, Image, Row, Text


def Testimonial(
    quote: Any,
    author: Any,
    *,
    avatar: Any = None,
    role: Any = None,
    **props: Any,
):
    """Create a reusable testimonial using existing PyLage components."""

    author_children = []

    if avatar is not None:
        if isinstance(avatar, str):
            author_children.append(Image(src=avatar, alt=str(author)))
        else:
            author_children.append(avatar)

    author_children.append(
        Column(
            Text(author),
            *([Text(role)] if role is not None else []),
        )
    )

    return Card(
        Column(
            Text(quote),
            Row(*author_children),
        ),
        **props,
    )
