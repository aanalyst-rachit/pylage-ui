"""Reusable pricing section pattern built on PyLage components."""

from typing import Any

from pylage.components import Badge, Button, Card, Column, Heading, Row, Text


def PricingSection(
    title: Any = "Choose Your Plan",
    description: Any = "Simple pricing for everyone.",
    plans: list[dict[str, Any]] | None = None,
    class_name: str = "pricing-section",
    **props: Any,
):
    """Create a reusable pricing section from PyLage primitives."""

    if plans is None:
        plans = [
            {
                "name": "Basic",
                "price": "$9",
                "description": "For individuals getting started.",
                "features": ["1 project", "Basic support"],
                "action": "Get Started",
            },
            {
                "name": "Pro",
                "price": "$29",
                "description": "For growing teams.",
                "features": ["10 projects", "Priority support"],
                "action": "Choose Pro",
                "featured": True,
            },
            {
                "name": "Enterprise",
                "price": "$99",
                "description": "For larger organizations.",
                "features": ["Unlimited projects", "Dedicated support"],
                "action": "Contact Us",
            },
        ]

    cards = []

    for plan in plans:
        children = [
            Heading(plan.get("name", "")),
            Text(plan.get("price", "")),
            Text(plan.get("description", "")),
        ]

        if plan.get("featured"):
            children.append(Badge("Popular"))

        for feature in plan.get("features", []):
            children.append(Text(feature))

        children.append(
            Button(plan.get("action", "Get Started"))
        )

        cards.append(
            Card(
                *children,
                class_name="pricing-card",
            )
        )

    return Column(
        Heading(title),
        Text(description),
        Row(*cards),
        class_name=class_name,
        **props,
    )
