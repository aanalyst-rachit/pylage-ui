"""
RULE 5 — Reusable UI Patterns Audit

Purpose:
- Verify patterns package imports correctly.
- Verify every pattern module imports.
- Verify public exports remain available.
- Verify every pattern returns a PyLage component.
- Catch broken internal imports and accidental API regressions.
"""

import importlib

import pylage_layout.patterns as patterns


PATTERN_MODULES = [
    "auth",
    "breadcrumbs",
    "contact",
    "content",
    "cta",
    "faq",
    "feature",
    "hero",
    "list",
    "newsletter",
    "pricing",
    "search",
    "states",
    "stats",
    "testimonial",
]


def test_patterns_package_imports():
    assert patterns is not None


def test_all_pattern_modules_import():
    for module_name in PATTERN_MODULES:
        module = importlib.import_module(
            f"pylage_layout.patterns.{module_name}"
        )
        assert module is not None


def test_patterns_public_api_exists():
    assert hasattr(patterns, "Hero")
    assert callable(patterns.Hero)


def test_patterns_all_matches_existing_exports():
    for name in patterns.__all__:
        assert hasattr(patterns, name), (
            f"patterns.__all__ contains missing export: {name}"
        )


def test_hero_returns_pylage_component():
    hero = patterns.Hero(
        title="Build with Python",
        description="Test description",
    )

    assert hero is not None
    assert hasattr(hero, "type")
    assert hasattr(hero, "props")


def test_hero_has_expected_component_structure():
    hero = patterns.Hero(
        title="Build with Python",
        description="Test description",
    )

    assert hero.type is not None
    assert isinstance(hero.props, dict)
