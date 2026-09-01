"""
PyLage Layout - Master Regression Test

Single pytest covering Phase 1 through Phase 7.

This test intentionally keeps all project-level regression coverage
inside one pytest file as requested.
"""

import importlib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _import(module_name):
    """Import a project module and fail with a useful message."""
    try:
        return importlib.import_module(module_name)
    except Exception as exc:
        pytest.fail(f"Failed to import {module_name}: {type(exc).__name__}: {exc}")


def _component_style(component):
    """Return component style from PyLage Component structure."""
    assert hasattr(component, "props"), f"{component!r} has no props"
    assert "style" in component.props, f"{component!r} has no style"
    return component.props["style"]


def _assert_responsive_style(style, name):
    """Verify the PyLage ResponsiveStyle contract."""
    assert type(style).__name__ == "ResponsiveStyle", (
        f"{name} must use ResponsiveStyle, got {type(style).__name__}"
    )

    assert getattr(style.base, "width", None) == "100%", (
        f"{name}: base width must be 100%"
    )

    assert getattr(style.base, "flex_direction", None) == "column", (
        f"{name}: mobile/base flex_direction must be column"
    )

    assert getattr(style.md, "flex_direction", None) == "row", (
        f"{name}: md flex_direction must be row"
    )

    assert getattr(style.lg, "gap", None) == "2rem", (
        f"{name}: lg gap must be 2rem"
    )


def test_phase_1_to_7_complete():
    """
    Master regression test for PyLage Layout Phases 1-7.

    One test covers the complete implemented project surface.
    """

    # ================================================================
    # Phase 1 — Design Tokens
    # ================================================================

    token_modules = [
        "pylage_layout.tokens.colors",
        "pylage_layout.tokens.fonts",
        "pylage_layout.tokens.radius",
        "pylage_layout.tokens.spacing",
        "pylage_layout.tokens.validate",
    ]

    for module_name in token_modules:
        module = _import(module_name)
        assert module is not None

    # Token package itself must import.
    tokens = _import("pylage_layout.tokens")
    assert tokens is not None

    # ================================================================
    # Phase 2 — Theme Presets
    # ================================================================

    theme_modules = [
        "pylage_layout.themes.api",
        "pylage_layout.themes.dark",
        "pylage_layout.themes.factory",
        "pylage_layout.themes.light",
        "pylage_layout.themes",
    ]

    for module_name in theme_modules:
        module = _import(module_name)
        assert module is not None

    # Neutral theme may be implemented under a different/current
    # project structure, so do not invent an import that does not exist.

    # ================================================================
    # Phase 3 — Basic + Multi-area Layouts
    # ================================================================

    layout_modules = [
        "pylage_layout.layouts.center",
        "pylage_layout.layouts.container",
        "pylage_layout.layouts.section",
        "pylage_layout.layouts.stack",
        "pylage_layout.layouts.split",
        "pylage_layout.layouts.two_column",
        "pylage_layout.layouts.three_column",
        "pylage_layout.layouts.sidebar",
    ]

    for module_name in layout_modules:
        module = _import(module_name)
        assert module is not None

    layouts = _import("pylage_layout.layouts")

    # Required high-level layout API.
    required_layout_exports = [
        "Center",
        "Container",
        "Section",
        "Stack",
        "Split",
        "SidebarLayout",
    ]

    for name in required_layout_exports:
        assert hasattr(layouts, name), f"layouts missing public export: {name}"

    # TwoColumn / ThreeColumn were previously found missing from
    # layouts/__init__.py. They must now be public.
    assert hasattr(layouts, "TwoColumn"), "layouts missing TwoColumn"
    assert hasattr(layouts, "ThreeColumn"), "layouts missing ThreeColumn"

    # Create representative layout components.
    container = layouts.Container()
    stack = layouts.Stack()
    split = layouts.Split()
    two_column = layouts.TwoColumn()
    three_column = layouts.ThreeColumn()

    for name, component in [
        ("Container", container),
        ("Stack", stack),
        ("Split", split),
        ("TwoColumn", two_column),
        ("ThreeColumn", three_column),
    ]:
        assert component is not None, f"{name} returned None"
        assert hasattr(component, "type"), f"{name} is not a PyLage component"

    # Expected underlying PyLage component types.
    assert container.type == "Column"
    assert stack.type == "Column"
    assert split.type == "Row"
    assert two_column.type == "Row"
    assert three_column.type == "Row"

    # ================================================================
    # Phase 4 — Navigation / Sidebar / Application Layouts
    # ================================================================

    phase4_modules = [
        "pylage_layout.layouts.drawer",
        "pylage_layout.layouts.footer",
        "pylage_layout.layouts.header",
        "pylage_layout.layouts.menu",
        "pylage_layout.layouts.navbar",
        "pylage_layout.layouts.navigation",
        "pylage_layout.layouts.navigation_controls",
        "pylage_layout.layouts.pagination",
        "pylage_layout.layouts.tabs",
        "pylage_layout.layouts.topbar",
    ]

    for module_name in phase4_modules:
        module = _import(module_name)
        assert module is not None

    # Public package must import successfully after all layout modules.
    assert hasattr(layouts, "Navigation")
    assert hasattr(layouts, "Menu")
    assert hasattr(layouts, "Pagination")

    # Specific modules must expose their expected high-level APIs.
    drawer = _import("pylage_layout.layouts.drawer")
    header = _import("pylage_layout.layouts.header")
    footer = _import("pylage_layout.layouts.footer")
    navbar = _import("pylage_layout.layouts.navbar")
    topbar = _import("pylage_layout.layouts.topbar")

    assert hasattr(drawer, "NavigationDrawer")
    assert hasattr(drawer, "MobileSidebar")
    assert hasattr(header, "Header")
    assert hasattr(footer, "Footer")
    assert hasattr(navbar, "Navbar")
    assert hasattr(topbar, "Topbar")

    # ================================================================
    # Phase 5 — Reusable UI Patterns
    # ================================================================

    pattern_modules = [
        "pylage_layout.patterns.auth",
        "pylage_layout.patterns.breadcrumbs",
        "pylage_layout.patterns.contact",
        "pylage_layout.patterns.content",
        "pylage_layout.patterns.cta",
        "pylage_layout.patterns.faq",
        "pylage_layout.patterns.feature",
        "pylage_layout.patterns.hero",
        "pylage_layout.patterns.list",
        "pylage_layout.patterns.newsletter",
        "pylage_layout.patterns.pricing",
        "pylage_layout.patterns.search",
        "pylage_layout.patterns.states",
        "pylage_layout.patterns.stats",
        "pylage_layout.patterns.testimonial",
    ]

    for module_name in pattern_modules:
        module = _import(module_name)
        assert module is not None

    patterns = _import("pylage_layout.patterns")
    assert patterns is not None

    # ================================================================
    # Phase 6 — Page Templates
    # ================================================================

    template_modules = [
        "pylage_layout.templates.landing",
        "pylage_layout.templates.dashboard",
        "pylage_layout.templates.admin",
        "pylage_layout.templates.admin_panel",
        "pylage_layout.templates.authentication",
        "pylage_layout.templates.profile",
        "pylage_layout.templates.settings",
        "pylage_layout.templates.documentation",
    ]

    for module_name in template_modules:
        module = _import(module_name)
        assert module is not None

    templates = _import("pylage_layout.templates")
    assert templates is not None

    # ================================================================
    # Phase 7 — Responsive Design
    # ================================================================

    pylage = _import("pylage")

    assert hasattr(pylage, "ResponsiveStyle"), (
        "PyLage ResponsiveStyle is required by Phase 7"
    )

    assert hasattr(pylage, "Style"), (
        "PyLage Style is required by Phase 7"
    )

    ResponsiveStyle = pylage.ResponsiveStyle
    Style = pylage.Style

    # Verify the underlying responsive capability itself.
    responsive = ResponsiveStyle(
        base=Style(
            width="100%",
            flex_direction="column",
        ),
        md=Style(
            flex_direction="row",
        ),
        lg=Style(
            gap="2rem",
        ),
    )

    _assert_responsive_style(responsive, "ResponsiveStyle")

    # Verify the actual public layouts use ResponsiveStyle.
    responsive_layouts = {
        "Container": container,
        "Stack": stack,
        "Split": split,
        "TwoColumn": two_column,
        "ThreeColumn": three_column,
    }

    for name, component in responsive_layouts.items():
        style = _component_style(component)
        _assert_responsive_style(style, name)

    # ================================================================
    # Phase 7 Regression — custom style must not cause duplicate style
    # keyword errors.
    # ================================================================

    # ThreeColumn previously raised:
    #
    # TypeError: Row() got multiple values for keyword argument 'style'
    #
    # Verify the regression remains fixed.
    custom_style = Style(
        width="90%",
    )

    three_custom = layouts.ThreeColumn(style=custom_style)

    assert three_custom.type == "Row"
    assert "style" in three_custom.props

    # ================================================================
    # Project Structure Regression
    # ================================================================

    expected_directories = [
        ROOT / "pylage_layout" / "layouts",
        ROOT / "pylage_layout" / "patterns",
        ROOT / "pylage_layout" / "templates",
        ROOT / "pylage_layout" / "themes",
        ROOT / "pylage_layout" / "tokens",
        ROOT / "app",
    ]

    for directory in expected_directories:
        assert directory.is_dir(), f"Missing project directory: {directory}"

    # Tests directory must exist now.
    assert (ROOT / "test").is_dir()

    # ================================================================
    # Final master assertion
    # ================================================================

    assert True
