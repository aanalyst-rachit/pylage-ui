"""Reusable feature-section pattern for PyLage Layout."""

from typing import Any

from pylage.components import Card, Column, Heading, Icon, Image, Row, Text


def FeatureSection(
    *features: Any,
    title: Any = None,
    description: Any = None,
    class_name: str | None = None,
    **props: Any,
):
    """Create a reusable feature section using PyLage components."""

    children = []

    if title is not None:
        children.append(Heading(title))

    if description is not None:
        children.append(Text(description))

    cards = []

    for feature in features:
        if isinstance(feature, dict):
            feature_children = []

            if feature.get("icon") is not None:
                feature_children.append(Icon(name=feature["icon"]))

            if feature.get("image") is not None:
                feature_children.append(
                    Image(
                        src=feature["image"],
                        alt=feature.get("title", ""),
                    )
                )

            if feature.get("title") is not None:
                feature_children.append(Heading(feature["title"]))

            if feature.get("description") is not None:
                feature_children.append(Text(feature["description"]))

            cards.append(Card(*feature_children))
        else:
            cards.append(Card(feature))

    if cards:
        children.append(Row(*cards))

    if class_name is not None:
        props["class_name"] = class_name

    return Column(*children, **props)
