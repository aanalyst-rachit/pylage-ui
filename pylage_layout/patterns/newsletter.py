"""Newsletter pattern for PyLage Layout."""

from typing import Any

from pylage.components import Button, Column, Form, Heading, Text


def NewsletterSection(
    title: Any = "Subscribe",
    description: Any = "Get the latest updates.",
    button_text: Any = "Subscribe",
    **props: Any,
):
    """Create a reusable newsletter signup section."""
    return Column(
        Heading(title),
        Text(description),
        Form(
            Text("Email"),
            Button(button_text),
        ),
        **props,
    )
