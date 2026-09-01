"""
RULE 5 — Reusable UI Patterns Audit

Purpose:
- Verify patterns package imports.
- Verify every implemented pattern module imports.
- Verify public exports exist.
- Verify exported patterns are callable.
- Verify basic component creation works.
- Catch future missing/renamed pattern regressions.
"""

import importlib

import pytest


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
    patterns = importlib.import_module("pylage_layout.patterns")
    assert patterns is not None


def test_pattern_modules_import():
    for module_name in PATTERN_MODULES:
        module = importlib.import_module(
            f"pylage_layout.patterns.{module_name}"
        )
        assert module is not None


def test_patterns_public_api_exists():
    patterns = importlib.import_module("pylage_layout.patterns")

    assert hasattr(patterns, "__all__")
    assert patterns.__all__

    for name in patterns.__all__:
        assert hasattr(patterns, name), (
            f"pylage_layout.patterns missing public export: {name}"
        )


def test_patterns_public_exports_are_callable():
    patterns = importlib.import_module("pylage_layout.patterns")

    for name in patterns.__all__:
        assert callable(getattr(patterns, name)), (
            f"Pattern export {name} must be callable"
        )


def test_hero_public_api():
    patterns = importlib.import_module("pylage_layout.patterns")

    assert hasattr(patterns, "Hero")

    hero = patterns.Hero(
        title="Build with Python",
        description="Test description",
        actions=[],
    )

    assert hero is not None
    assert hasattr(hero, "type")
    assert hasattr(hero, "props")


def test_pattern_modules_have_public_symbols():
    for module_name in PATTERN_MODULES:
        module = importlib.import_module(
            f"pylage_layout.patterns.{module_name}"
        )

        public_names = [
            name
            for name in dir(module)
            if not name.startswith("_")
        ]

        assert public_names, (
            f"Pattern module {module_name} exposes no public symbols"
        )
