"""Common UI state patterns for PyLage Layout."""

from typing import Any

from pylage.components import Column, Heading, Text


def EmptyState(
    title: Any = "Nothing here",
    description: Any = "There is no content to display.",
    **props: Any,
):
    return Column(
        Heading(title),
        Text(description),
        **props,
    )


def ErrorState(
    title: Any = "Something went wrong",
    description: Any = "Please try again.",
    **props: Any,
):
    return Column(
        Heading(title),
        Text(description),
        **props,
    )


def Loading(
    text: Any = "Loading...",
    **props: Any,
):
    return Column(
        Text(text),
        **props,
    )
