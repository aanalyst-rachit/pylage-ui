"""Authentication page template for PyLage Layout."""

from typing import Any

from ..layouts import Container
from pylage.components import (
    Button,
    Card,
    Column,
    Form,
    Heading,
    Input,
    Text,
)


def Authentication(
    title: Any = "Welcome back",
    description: Any = "Sign in to continue.",
    form: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a reusable authentication page."""

    if form is None:
        form = Form(
            Input(
                "",
                class_name="auth-email",
                title="Email",
            ),
            Input(
                "",
                class_name="auth-password",
                title="Password",
            ),
            Button(
                "Sign In",
                class_name="auth-submit",
            ),
            class_name="auth-form",
        )

    content = Column(
        Heading(title),
        Text(description),
        Card(
            form,
            class_name="auth-card",
        ),
        footer if footer is not None else Text(""),
        class_name="auth-content",
    )

    return Container(
        content,
        **props,
    )
