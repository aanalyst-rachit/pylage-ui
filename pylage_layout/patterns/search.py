"""Search pattern for PyLage Layout."""

from typing import Any

from pylage.components import Button, Form, Row, Text


def SearchBar(
    placeholder: Any = "Search",
    button_text: Any = "Search",
    **props: Any,
):
    """Create a reusable search bar using PyLage components."""
    return Form(
        Row(
            Text(placeholder),
            Button(button_text),
        ),
        **props,
    )
