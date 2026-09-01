"""
RULE 3 — Layouts Audit

Purpose:
- Verify all layout modules import correctly.
- Verify the public layouts API remains stable.
- Verify representative layouts create valid PyLage components.
- Verify expected underlying component types.
- Verify ResponsiveStyle contract.
- Verify custom style regression remains fixed.
"""

import importlib

import pylage_layout.layouts as layouts
from pylage import ResponsiveStyle, Style


LAYOUT_MODULES = [
    "center",
    "container",
    "section",
    "stack",
    "split",
    "two_column",
    "three_column",
    "sidebar",
    "drawer",
    "footer",
    "header",
    "menu",
    "navbar",
    "navigation",
    "navigation_controls",
    "pagination",
    "tabs",
    "topbar",
]


def test_all_layout_modules_import():
    for module_name in LAYOUT_MODULES:
        module = importlib.import_module(
            f"pylage_layout.layouts.{module_name}"
        )
        assert module is not None


def test_layout_public_api_exists():
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

    assert set(layouts.__all__) == expected

    for name in expected:
        assert hasattr(layouts, name), (
            f"layouts missing public export: {name}"
        )


def test_basic_layout_component_types():
    cases = {
        "Container": ("Column", layouts.Container()),
        "Stack": ("Column", layouts.Stack()),
        "Split": ("Row", layouts.Split()),
        "TwoColumn": ("Row", layouts.TwoColumn()),
        "ThreeColumn": ("Row", layouts.ThreeColumn()),
    }

    for name, (expected_type, component) in cases.items():
        assert component is not None
        assert hasattr(component, "type"), (
            f"{name} did not return a PyLage component"
        )
        assert component.type == expected_type, (
            f"{name}: expected {expected_type}, got {component.type}"
        )


def test_responsive_style_contract():
    components = {
        "Container": layouts.Container(),
        "Stack": layouts.Stack(),
        "Split": layouts.Split(),
        "TwoColumn": layouts.TwoColumn(),
        "ThreeColumn": layouts.ThreeColumn(),
    }

    for name, component in components.items():
        assert hasattr(component, "props"), f"{name} has no props"
        assert "style" in component.props, f"{name} has no style"

        style = component.props["style"]

        assert type(style).__name__ == "ResponsiveStyle", (
            f"{name} must use ResponsiveStyle"
        )

        assert getattr(style.base, "width", None) == "100%", (
            f"{name}: base width must be 100%"
        )

        assert getattr(style.base, "flex_direction", None) == "column", (
            f"{name}: base flex_direction must be column"
        )

        assert getattr(style.md, "flex_direction", None) == "row", (
            f"{name}: md flex_direction must be row"
        )

        assert getattr(style.lg, "gap", None) == "2rem", (
            f"{name}: lg gap must be 2rem"
        )


def test_responsive_style_itself_works():
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

    assert type(responsive).__name__ == "ResponsiveStyle"
    assert responsive.base.width == "100%"
    assert responsive.base.flex_direction == "column"
    assert responsive.md.flex_direction == "row"
    assert responsive.lg.gap == "2rem"


def test_three_column_custom_style_regression():
    custom_style = Style(width="90%")

    component = layouts.ThreeColumn(style=custom_style)

    assert component is not None
    assert component.type == "Row"
    assert "style" in component.props
