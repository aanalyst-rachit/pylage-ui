"""Theme construction helpers for PyLage Layout."""

from pylage import Theme

from ..tokens import COLORS, FONTS, RADIUS, SPACING


def create_theme(
    *,
    name: str,
    colors: dict,
) -> Theme:
    """Create a PyLage Theme from PyLage Layout design tokens."""
    return Theme(
        name=name,
        colors=colors,
        spacing=SPACING,
        radius=RADIUS,
        fonts=FONTS,
    )


__all__ = ["create_theme"]
