"""
RULE 9 — Testing Audit

Purpose:
- Verify public PyLage Layout features have behavior-focused regression tests.
- Test behavior introduced by pylage_layout only.
- Do not duplicate PyLage framework tests.

Coverage:
- construction
- props
- children
- rendering
- themes
- responsive behavior
- composition
- regression cases
"""

import pylage_layout
import pylage_layout.layouts as layouts
import pylage_layout.patterns as patterns
import pylage_layout.themes as themes
import pylage_layout.tokens as tokens
import pylage_layout.templates as templates

from pylage import ResponsiveStyle, Style
from pylage.components import Text


# ================================================================
# Construction
# ================================================================

def test_public_layout_construction():
    components = [
        layouts.Center(),
        layouts.Container(),
        layouts.Section(),
        layouts.Stack(),
        layouts.Split(),
        layouts.TwoColumn(),
        layouts.ThreeColumn(),
    ]

    for component in components:
        assert component is not None
        assert hasattr(component, "type")


def test_public_pattern_construction():
    hero = patterns.Hero(
        title="Build with Python",
        description="Reusable hero pattern.",
    )

    assert hero is not None
    assert hasattr(hero, "type")


def test_public_template_construction():
    landing = templates.LandingPage()

    assert landing is not None
    assert hasattr(landing, "type")


# ================================================================
# Props
# ================================================================

def test_layout_custom_props_are_preserved():
    component = layouts.Container(
        id="test-container",
    )

    assert component.props.get("id") == "test-container"


def test_hero_custom_props_are_preserved():
    hero = patterns.Hero(
        title="Hello",
        data_test="hero",
    )

    assert hero.props.get("data_test") == "hero"


# ================================================================
# Children
# ================================================================

def test_layout_children_are_composed():
    child = Text("Child")

    component = layouts.Container(
        child,
    )

    assert child in component.children


def test_hero_contains_title_and_description():
    hero = patterns.Hero(
        title="Build with Python",
        description="Create reusable interfaces.",
    )

    assert len(hero.children) >= 2

    child_types = [child.type for child in hero.children]

    assert "Heading" in child_types
    assert "Text" in child_types


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
    assert header in app.children

    assert len(app.children) >= 2

    content_area = app.children[1]

    assert sidebar in content_area.children
    assert content in content_area.children


# ================================================================
# Rendering / component shape
# ================================================================

def test_public_layouts_produce_components():
    components = [
        layouts.Center(),
        layouts.Container(),
        layouts.Section(),
        layouts.Stack(),
        layouts.Split(),
        layouts.TwoColumn(),
        layouts.ThreeColumn(),
    ]

    for component in components:
        assert isinstance(component.type, str)
        assert component.type


def test_hero_produces_column_component():
    hero = patterns.Hero(
        title="Build with Python",
    )

    assert hero.type == "Column"


# ================================================================
# Themes
# ================================================================

def test_light_and_dark_themes_are_registered():
    available = themes.available_themes()

    assert "light" in available
    assert "dark" in available


def test_get_theme_returns_requested_theme():
    light = themes.get_theme("light")
    dark = themes.get_theme("dark")

    assert light.name == "light"
    assert dark.name == "dark"


def test_theme_colors_are_distinct():
    light = themes.get_theme("light")
    dark = themes.get_theme("dark")

    assert light.colors != dark.colors


# ================================================================
# Responsive behavior
# ================================================================

def test_public_layouts_use_responsive_styles():
    components = {
        "Container": layouts.Container(),
        "Stack": layouts.Stack(),
        "Split": layouts.Split(),
        "TwoColumn": layouts.TwoColumn(),
        "ThreeColumn": layouts.ThreeColumn(),
    }

    for name, component in components.items():
        style = component.props.get("style")

        assert isinstance(
            style,
            ResponsiveStyle,
        ), f"{name} must use ResponsiveStyle"


def test_responsive_style_can_be_composed():
    responsive = ResponsiveStyle(
        base=Style(
            width="100%",
            flex_direction="column",
        ),
        md=Style(
            flex_direction="row",
        ),
    )

    assert responsive is not None
    assert hasattr(responsive, "base")
    assert hasattr(responsive, "md")


# ================================================================
# Composition
# ================================================================

def test_layouts_can_be_nested():
    inner = layouts.Stack(
        Text("Inner"),
    )

    outer = layouts.Container(
        inner,
    )

    assert inner in outer.children


def test_hero_can_accept_component_actions():
    action = Text("Action")

    hero = patterns.Hero(
        title="Build",
        actions=[action],
    )

    assert hero is not None
    assert len(hero.children) >= 2

    action_row = hero.children[-1]

    assert action in action_row.children


# ================================================================
# Regression cases
# ================================================================

def test_three_column_custom_style_does_not_duplicate_style_keyword():
    custom_style = Style(
        width="90%",
    )

    component = layouts.ThreeColumn(
        style=custom_style,
    )

    assert component.type == "Row"
    assert component.props.get("style") is custom_style


def test_public_package_does_not_require_internal_imports():
    assert hasattr(pylage_layout, "layouts")
    assert hasattr(pylage_layout, "patterns")
    assert hasattr(pylage_layout, "themes")
    assert hasattr(pylage_layout, "tokens")
    assert hasattr(pylage_layout, "templates")


def test_token_validation_remains_available():
    result = tokens.validate_tokens()

    assert result is None or result is True
