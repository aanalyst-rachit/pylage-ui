"""Contact section pattern for PyLage Layout."""

from typing import Any

from pylage.components import Button, Column, Form, Heading, Text


def ContactSection(
    title: Any = "Contact Us",
    description: Any = "Get in touch with us.",
    button_text: Any = "Send Message",
    **props: Any,
):
    """Create a reusable contact section using PyLage components."""
    return Column(
        Heading(title),
        Text(description),
        Form(
            Text("Name"),
            Text("Email"),
            Text("Message"),
            Button(button_text),
        ),
        **props,
    )
