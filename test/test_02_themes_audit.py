"""
RULE 3 — Themes Audit

Purpose:
- Verify themes package imports correctly.
- Verify public theme API remains stable.
- Verify light and dark themes exist.
- Verify available_themes() remains deterministic.
- Verify get_theme() returns the correct theme.
- Verify unknown theme names fail clearly.
- Verify theme objects contain required token sections.
- Verify create_theme() remains functional.
"""

import pytest

import pylage_layout.themes as themes
from pylage_layout.themes.factory import create_theme


def test_themes_package_imports():
    assert themes is not None


def test_themes_public_api_exists():
    expected = {
        "DARK_COLORS",
        "DARK_THEME",
        "LIGHT_COLORS",
        "LIGHT_THEME",
        "available_themes",
        "get_theme",
    }

    for name in expected:
        assert hasattr(themes, name), (
            f"pylage_layout.themes missing public export: {name}"
        )


def test_themes_all_matches_public_api():
    expected = {
        "DARK_COLORS",
        "DARK_THEME",
        "LIGHT_COLORS",
        "LIGHT_THEME",
        "available_themes",
        "get_theme",
    }

    assert set(themes.__all__) == expected


def test_available_themes():
    result = themes.available_themes()

    assert isinstance(result, tuple)
    assert result == ("dark", "light")


def test_get_light_theme():
    theme = themes.get_theme("light")

    assert theme is themes.LIGHT_THEME
    assert theme.name == "light"


def test_get_dark_theme():
    theme = themes.get_theme("dark")

    assert theme is themes.DARK_THEME
    assert theme.name == "dark"


def test_unknown_theme_raises_value_error():
    with pytest.raises(ValueError, match="Unknown theme"):
        themes.get_theme("unknown")


def test_light_theme_contains_required_sections():
    theme = themes.LIGHT_THEME

    assert theme.colors
    assert theme.spacing
    assert theme.radius
    assert theme.fonts


def test_dark_theme_contains_required_sections():
    theme = themes.DARK_THEME

    assert theme.colors
    assert theme.spacing
    assert theme.radius
    assert theme.fonts


def test_dark_and_light_themes_are_distinct():
    assert themes.LIGHT_THEME is not themes.DARK_THEME
    assert themes.LIGHT_THEME.name != themes.DARK_THEME.name
    assert themes.LIGHT_THEME.colors != themes.DARK_THEME.colors


def test_light_colors_match_light_theme():
    assert dict(themes.LIGHT_THEME.colors) == themes.LIGHT_COLORS


def test_dark_colors_match_dark_theme():
    assert dict(themes.DARK_THEME.colors) == themes.DARK_COLORS


def test_create_theme():
    custom_colors = {
        "background": "#000000",
        "surface": "#111111",
        "surface_alt": "#222222",
        "text": "#ffffff",
        "text_muted": "#cccccc",
        "border": "#333333",
        "primary": "#ff0000",
        "secondary": "#00ff00",
        "success": "#00ffff",
        "warning": "#ffff00",
        "danger": "#ff00ff",
        "info": "#123456",
    }

    theme = create_theme(
        name="audit-test",
        colors=custom_colors,
    )

    assert theme.name == "audit-test"
    assert dict(theme.colors) == custom_colors
    assert theme.spacing
    assert theme.radius
    assert theme.fonts
