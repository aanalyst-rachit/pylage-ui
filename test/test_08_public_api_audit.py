"""
RULE 8 — Public API Audit

Purpose:
- Verify the public layouts API is simple and importable.
- Verify AppShell is publicly available from pylage_layout.layouts.
- Verify AppShell accepts header/sidebar/content composition.
- Verify reusable Hero is publicly available.
- Verify Hero supports title, description, and actions.
- Prevent accidental removal of Phase 8 public API.
"""

from pylage import Button, Text

import pylage_layout.layouts as layouts
import pylage_layout.patterns as patterns


def test_layouts_package_imports():
    assert layouts is not None


def test_patterns_package_imports():
    assert patterns is not None


def test_app_shell_is_public():
    assert hasattr(layouts, "AppShell"), (
        "layouts.AppShell must be part of the public Phase 8 API"
    )


def test_app_shell_is_callable():
    assert callable(layouts.AppShell)


def test_app_shell_composes_header_sidebar_content():
    header = Text("Header")
    sidebar = Text("Sidebar")
    content = Text("Content")

    app = layouts.AppShell(
        header=header,
        sidebar=sidebar,
        content=content,
    )

    assert app is not None
    assert hasattr(app, "type")
    assert hasattr(app, "props")


def test_hero_is_public():
    assert hasattr(patterns, "Hero"), (
        "patterns.Hero must be part of the public Phase 8 API"
    )


def test_hero_is_callable():
    assert callable(patterns.Hero)


def test_hero_supports_target_usage():
    hero = patterns.Hero(
        title="Build with Python",
        description="Build reusable layouts with Python.",
        actions=[
            Button("Get Started"),
            Button("Learn More"),
        ],
    )

    assert hero is not None
    assert hasattr(hero, "type")
    assert hasattr(hero, "props")


def test_hero_accepts_string_actions():
    hero = patterns.Hero(
        title="Build with Python",
        actions=["Get Started", "Learn More"],
    )

    assert hero is not None
    assert hasattr(hero, "type")


def test_public_layout_all_contains_app_shell():
    assert "AppShell" in layouts.__all__


def test_public_pattern_all_contains_hero():
    assert "Hero" in patterns.__all__


def test_public_api_does_not_require_internal_imports():
    # Public consumers should never need:
    # from layouts import ...
    # from patterns import ...
    # They should use pylage_layout.layouts / pylage_layout.patterns.
    from pylage_layout.layouts import AppShell
    from pylage_layout.patterns import Hero

    assert callable(AppShell)
    assert callable(Hero)
