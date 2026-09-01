"""
RULE 2 — Design Tokens Audit

Purpose:
- Verify token subpackage imports correctly.
- Verify all public token exports exist.
- Verify token collections are non-empty.
- Verify expected core token keys remain available.
- Verify validate_tokens() continues to work.

This is a dedicated regression test for Phase 1.
"""

import pylage_layout.tokens as tokens


def test_tokens_package_imports():
    assert tokens is not None


def test_tokens_public_api_exists():
    expected = [
        "COLORS",
        "FONTS",
        "RADIUS",
        "SPACING",
        "validate_tokens",
    ]

    for name in expected:
        assert hasattr(tokens, name), (
            f"pylage_layout.tokens missing public export: {name}"
        )


def test_tokens_all_matches_public_api():
    expected = {
        "COLORS",
        "FONTS",
        "RADIUS",
        "SPACING",
        "validate_tokens",
    }

    assert set(tokens.__all__) == expected


def test_colors_are_available():
    assert isinstance(tokens.COLORS, dict)
    assert tokens.COLORS

    required_keys = {
        "background",
        "surface",
        "text",
        "text_muted",
        "border",
        "primary",
        "secondary",
        "success",
        "warning",
        "danger",
        "info",
    }

    assert required_keys.issubset(tokens.COLORS.keys())


def test_fonts_are_available():
    assert isinstance(tokens.FONTS, dict)
    assert tokens.FONTS

    required_keys = {"sans", "serif", "mono"}
    assert required_keys.issubset(tokens.FONTS.keys())


def test_radius_are_available():
    assert isinstance(tokens.RADIUS, dict)
    assert tokens.RADIUS

    required_keys = {
        "none",
        "sm",
        "md",
        "lg",
        "xl",
        "2xl",
        "full",
    }

    assert required_keys.issubset(tokens.RADIUS.keys())


def test_spacing_are_available():
    assert isinstance(tokens.SPACING, dict)
    assert tokens.SPACING

    required_keys = {
        "0",
        "xs",
        "sm",
        "md",
        "lg",
        "xl",
        "2xl",
        "3xl",
        "4xl",
    }

    assert required_keys.issubset(tokens.SPACING.keys())


def test_validate_tokens_is_callable():
    assert callable(tokens.validate_tokens)


def test_validate_tokens_passes():
    result = tokens.validate_tokens()
    assert result is None or result is True
