"""Reusable FAQ pattern built on PyLage components."""

from typing import Any

from pylage.components import Accordion, Heading, Text


def FAQ(
    title: Any = "Frequently Asked Questions",
    items: list[tuple[Any, Any]] | None = None,
    **props: Any,
):
    """Create a reusable FAQ section using PyLage Accordion."""
    if items is None:
        items = [
            ("What is PyLage?", "PyLage is a Python UI framework."),
            ("What is pylage_layout?", "pylage_layout provides reusable layouts and UI patterns."),
        ]

    questions = []

    for question, answer in items:
        questions.append(
            Text(
                f"{question}: {answer}",
            )
        )

    return Accordion(
        Heading(title),
        *questions,
        class_name=props.pop("class_name", "faq-section"),
        **props,
    )
