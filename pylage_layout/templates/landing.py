"""Landing page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from ..patterns import Hero, FeatureSection, StatsSection, PricingSection, CTA
from ..layouts import Footer


def LandingPage(
    hero: Any = None,
    features: Any = None,
    stats: Any = None,
    pricing: Any = None,
    cta: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a complete landing page from PyLage Layout patterns."""

    children = []

    if hero is not None:
        children.append(hero)

    if features is not None:
        children.append(features)

    if stats is not None:
        children.append(stats)

    if pricing is not None:
        children.append(pricing)

    if cta is not None:
        children.append(cta)

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(*children, **props)
    )
