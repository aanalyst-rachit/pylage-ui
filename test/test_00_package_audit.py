"""
PyLage Layout — Package/API Audit

Permanent regression rules for the public package surface.

This test must fail if:
- top-level package stops importing
- public subpackages disappear
- documented public exports disappear
- __all__ becomes inconsistent
- legacy top-level imports are accidentally restored
- package modules cannot be imported through pylage_layout.*
"""

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "pylage_layout"


def _import(name):
    """Import a module and return it with a useful failure."""
    try:
        return importlib.import_module(name)
    except Exception as exc:
        raise AssertionError(
            f"Failed to import {name}: {type(exc).__name__}: {exc}"
        ) from exc


# ======================================================================
# RULE 1 — Top-level package must exist and import
# ======================================================================

def test_top_level_package_exists():
    assert PACKAGE.is_dir(), "pylage_layout package directory is missing"
    assert (PACKAGE / "__init__.py").is_file(), (
        "pylage_layout/__init__.py is missing"
    )


def test_top_level_package_imports():
    package = _import("pylage_layout")

    assert package.__file__ is not None
    assert package.__file__.endswith("pylage_layout/__init__.py")


# ======================================================================
# RULE 2 — Required public subpackages
# ======================================================================

def test_required_subpackages_import():
    required = [
        "layouts",
        "patterns",
        "themes",
        "tokens",
        "templates",
    ]

    package = _import("pylage_layout")

    for name in required:
        assert hasattr(package, name), (
            f"pylage_layout missing public subpackage: {name}"
        )

        module = _import(f"pylage_layout.{name}")
        assert module is not None


# ======================================================================
# RULE 3 — Top-level __all__ must match public subpackages
# ======================================================================

def test_top_level_all():
    package = _import("pylage_layout")

    expected = {
        "layouts",
        "patterns",
        "themes",
        "tokens",
        "templates",
    }

    actual = set(getattr(package, "__all__", []))

    assert actual == expected, (
        "pylage_layout.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )


# ======================================================================
# RULE 4 — Every symbol in top-level __all__ must exist
# ======================================================================

def test_top_level_all_symbols_exist():
    package = _import("pylage_layout")

    for name in package.__all__:
        assert hasattr(package, name), (
            f"pylage_layout.__all__ contains missing symbol: {name}"
        )


# ======================================================================
# RULE 5 — Layout public API
# ======================================================================

def test_layout_public_api():
    layouts = _import("pylage_layout.layouts")

    expected = {
        "AppShell",
        "Center",
        "Container",
        "Footer",
        "Header",
        "Navigation",
        "Pagination",
        "Menu",
        "Section",
        "SidebarLayout",
        "Split",
        "Stack",
        "TwoColumn",
        "ThreeColumn",
    }

    actual = set(getattr(layouts, "__all__", []))

    assert actual == expected, (
        "layouts.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )

    for name in expected:
        assert hasattr(layouts, name), (
            f"layouts missing public symbol: {name}"
        )


# ======================================================================
# RULE 6 — Patterns public API
# ======================================================================

def test_patterns_public_api():
    patterns = _import("pylage_layout.patterns")

    expected = {
        "Hero",
    }

    actual = set(getattr(patterns, "__all__", []))

    assert actual == expected, (
        "patterns.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )

    for name in expected:
        assert hasattr(patterns, name), (
            f"patterns missing public symbol: {name}"
        )


# ======================================================================
# RULE 7 — Themes public API
# ======================================================================

def test_themes_public_api():
    themes = _import("pylage_layout.themes")

    expected = {
        "DARK_COLORS",
        "DARK_THEME",
        "LIGHT_COLORS",
        "LIGHT_THEME",
        "available_themes",
        "get_theme",
    }

    actual = set(getattr(themes, "__all__", []))

    assert actual == expected, (
        "themes.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )

    for name in expected:
        assert hasattr(themes, name), (
            f"themes missing public symbol: {name}"
        )


# ======================================================================
# RULE 8 — Tokens public API
# ======================================================================

def test_tokens_public_api():
    tokens = _import("pylage_layout.tokens")

    expected = {
        "COLORS",
        "FONTS",
        "RADIUS",
        "SPACING",
        "validate_tokens",
    }

    actual = set(getattr(tokens, "__all__", []))

    assert actual == expected, (
        "tokens.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )

    for name in expected:
        assert hasattr(tokens, name), (
            f"tokens missing public symbol: {name}"
        )


# ======================================================================
# RULE 9 — Templates public API
# ======================================================================

def test_templates_public_api():
    templates = _import("pylage_layout.templates")

    expected = {
        "LandingPage",
        "Dashboard",
        "AdminPanel",
        "Authentication",
        "ProfilePage",
    }

    actual = set(getattr(templates, "__all__", []))

    assert actual == expected, (
        "templates.__all__ mismatch\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}"
    )

    for name in expected:
        assert hasattr(templates, name), (
            f"templates missing public symbol: {name}"
        )


# ======================================================================
# RULE 10 — Important internal modules must import through package path
# ======================================================================

def test_core_modules_import_through_package():
    modules = [
        # Tokens
        "pylage_layout.tokens.colors",
        "pylage_layout.tokens.fonts",
        "pylage_layout.tokens.radius",
        "pylage_layout.tokens.spacing",
        "pylage_layout.tokens.validate",

        # Themes
        "pylage_layout.themes.api",
        "pylage_layout.themes.dark",
        "pylage_layout.themes.factory",
        "pylage_layout.themes.light",

        # Layouts
        "pylage_layout.layouts.center",
        "pylage_layout.layouts.container",
        "pylage_layout.layouts.drawer",
        "pylage_layout.layouts.footer",
        "pylage_layout.layouts.header",
        "pylage_layout.layouts.menu",
        "pylage_layout.layouts.navbar",
        "pylage_layout.layouts.navigation",
        "pylage_layout.layouts.navigation_controls",
        "pylage_layout.layouts.pagination",
        "pylage_layout.layouts.section",
        "pylage_layout.layouts.sidebar",
        "pylage_layout.layouts.split",
        "pylage_layout.layouts.stack",
        "pylage_layout.layouts.tabs",
        "pylage_layout.layouts.topbar",
        "pylage_layout.layouts.two_column",
        "pylage_layout.layouts.three_column",

        # Patterns
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

        # Templates
        "pylage_layout.templates.admin",
        "pylage_layout.templates.admin_panel",
        "pylage_layout.templates.authentication",
        "pylage_layout.templates.dashboard",
        "pylage_layout.templates.documentation",
        "pylage_layout.templates.landing",
        "pylage_layout.templates.profile",
        "pylage_layout.templates.settings",
    ]

    for module_name in modules:
        module = _import(module_name)
        assert module is not None


# ======================================================================
# RULE 11 — No legacy sibling-package imports inside pylage_layout
# ======================================================================

def test_no_legacy_sibling_imports():
    forbidden_patterns = [
        "from tokens import",
        "import tokens",
        "from themes import",
        "import themes",
        "from layouts import",
        "import layouts",
        "from patterns import",
        "import patterns",
        "from templates import",
        "import templates",
    ]

    package_files = PACKAGE.rglob("*.py")

    violations = []

    for file_path in package_files:
        text = file_path.read_text(encoding="utf-8")

        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()

            for pattern in forbidden_patterns:
                if stripped.startswith(pattern):
                    violations.append(
                        f"{file_path.relative_to(ROOT)}:"
                        f"{line_number}: {stripped}"
                    )

    assert not violations, (
        "Legacy sibling-package imports detected:\n"
        + "\n".join(violations)
    )


# ======================================================================
# RULE 12 — Tests must use package-qualified imports
# ======================================================================

def test_test_suite_uses_package_imports():
    tests_dir = ROOT / "tests"

    forbidden_patterns = [
        "from tokens import",
        "import tokens",
        "from themes import",
        "import themes",
        "from layouts import",
        "import layouts",
        "from patterns import",
        "import patterns",
        "from templates import",
        "import templates",
    ]

    violations = []

    for file_path in tests_dir.rglob("*.py"):
        text = file_path.read_text(encoding="utf-8")

        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()

            for pattern in forbidden_patterns:
                if stripped.startswith(pattern):
                    violations.append(
                        f"{file_path.relative_to(ROOT)}:"
                        f"{line_number}: {stripped}"
                    )

    assert not violations, (
        "Tests contain legacy imports:\n"
        + "\n".join(violations)
    )
