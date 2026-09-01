"""Reusable statistics section pattern for PyLage Layout."""

from typing import Any, Iterable, Mapping

from pylage.components import Card, Column, Heading, Row, Text


def StatsSection(
    title: str = "Stats",
    description: str | None = None,
    stats: Iterable[Mapping[str, Any]] = (),
    **props: Any,
):
    """Create a reusable statistics section using PyLage components.

    Each stat mapping may contain:
        value: Main statistic value.
        label: Statistic label.
        description: Optional supporting text.
    """
    cards = []

    for stat in stats:
        value = stat.get("value", "")
        label = stat.get("label", "")
        stat_description = stat.get("description")

        children = [
            Heading(value),
            Text(label),
        ]

        if stat_description is not None:
            children.append(Text(stat_description))

        cards.append(Card(*children))

    content = [
        Heading(title),
    ]

    if description is not None:
        content.append(Text(description))

    content.append(Row(*cards))

    return Column(
        *content,
        class_name=props.pop("class_name", "stats-section"),
        **props,
    )
