"""Public theme API for PyLage Layout."""

from pylage import Theme

from .dark import DARK_THEME
from .light import LIGHT_THEME


_THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
}


def get_theme(name: str) -> Theme:
    """Return a registered PyLage Layout theme by name."""
    try:
        return _THEMES[name]
    except KeyError:
        available = ", ".join(sorted(_THEMES))
        raise ValueError(
            f"Unknown theme: {name!r}. Available themes: {available}"
        ) from None


def available_themes() -> tuple[str, ...]:
    """Return the names of all registered themes."""
    return tuple(sorted(_THEMES))


__all__ = [
    "DARK_THEME",
    "LIGHT_THEME",
    "available_themes",
    "get_theme",
]
