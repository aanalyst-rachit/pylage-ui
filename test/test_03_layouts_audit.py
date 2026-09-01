"""
RULE 4 — Layouts Audit

Purpose:
- Verify layouts package imports.
- Verify every required layout module exists.
- Verify public exports remain available.
- Verify layout factories return PyLage components.
- Verify expected underlying component types.
- Verify responsive styles remain attached.
- Verify custom styles do not cause duplicate keyword errors.
"""

import importlib

import pylage_layout.layouts as layouts
from pylage import ResponsiveStyle, Style


REQUIRED_MODULES = [
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

REQUIRED_EXPORTS = [
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
]


def test_layouts_package_imports():
    assert layouts is not None


def test_required_layout_modules_import():
    for module_name in REQUIRED_MODULES:
        module = importlib.import_module(
            f"pylage_layout.layouts.{module_name}"
        )
        assert module is not None


def test_required_public_exports_exist():
    for name in REQUIRED_EXPORTS:
        assert hasattr(layouts, name), (
            f"layouts missing public export: {name}"
        )


def test_layouts_all_contains_required_exports():
    assert set(REQUIRED_EXPORTS).issubset(set(layouts.__all__))


def test_layout_factories_return_components():
    components = {
        "Center": layouts.Center(),
        "Container": layouts.Container(),
        "Section": layouts.Section(),
        "Stack": layouts.Stack(),
        "Split": layouts.Split(),
        "SidebarLayout": layouts.SidebarLayout(sidebar=layouts.Container(), content=layouts.Container()),
        "TwoColumn": layouts.TwoColumn(),
        "ThreeColumn": layouts.ThreeColumn(),
    }

    for name, component in components.items():
        assert component is not None, f"{name} returned None"
        assert hasattr(component, "type"), (
            f"{name} is not a PyLage component"
        )


def test_expected_component_types():
    assert layouts.Container().type == "Column"
    assert layouts.Stack().type == "Column"
    assert layouts.Section().type == "Column"
    assert layouts.Split().type == "Row"
    assert layouts.TwoColumn().type == "Row"
    assert layouts.ThreeColumn().type == "Row"


def _component_style(component):
    props = getattr(component, "props", {})
    return props.get("style")


def test_layouts_use_responsive_style():
    components = {
        "Container": layouts.Container(),
        "Stack": layouts.Stack(),
        "Split": layouts.Split(),
        "TwoColumn": layouts.TwoColumn(),
        "ThreeColumn": layouts.ThreeColumn(),
    }

    for name, component in components.items():
        style = _component_style(component)

        assert style is not None, (
            f"{name} has no style"
        )

        assert isinstance(style, ResponsiveStyle), (
            f"{name} does not use ResponsiveStyle"
        )


def test_responsive_style_is_constructible():
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

    assert responsive is not None


def test_three_column_custom_style_regression():
    custom_style = Style(
        width="90%",
    )

    component = layouts.ThreeColumn(
        style=custom_style,
    )

    assert component.type == "Row"
    assert "style" in component.props
