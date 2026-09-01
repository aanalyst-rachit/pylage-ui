"""Authentication patterns for PyLage Layout."""

from typing import Any

from pylage.components import Button, Column, Form, Heading, Text


def LoginForm(
    title: Any = "Login",
    button_text: Any = "Login",
    **props: Any,
):
    """Create a reusable login form."""
    return Column(
        Heading(title),
        Form(
            Text("Email"),
            Text("Password"),
            Button(button_text),
        ),
        **props,
    )


def SignupForm(
    title: Any = "Create Account",
    button_text: Any = "Sign Up",
    **props: Any,
):
    """Create a reusable signup form."""
    return Column(
        Heading(title),
        Form(
            Text("Name"),
            Text("Email"),
            Text("Password"),
            Button(button_text),
        ),
        **props,
    )
