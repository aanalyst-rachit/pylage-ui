"""
RULE 7 — Page Templates Audit

Purpose:
- Verify templates package imports.
- Verify every required template module exists.
- Verify public template exports.
- Verify __all__ is accurate.
- Verify every template is callable.
- Verify every template returns a PyLage component.
"""

import importlib

import pytest


TEMPLATE_MODULES = [
    "landing",
    "dashboard",
    "admin",
    "admin_panel",
    "authentication",
    "profile",
    "settings",
    "documentation",
]

PUBLIC_TEMPLATES = [
    "LandingPage",
    "Dashboard",
    "AdminPanel",
    "Authentication",
    "ProfilePage",
]


def test_templates_package_imports():
    templates = importlib.import_module("pylage_layout.templates")
    assert templates is not None


@pytest.mark.parametrize("module_name", TEMPLATE_MODULES)
def test_template_module_imports(module_name):
    module = importlib.import_module(
        f"pylage_layout.templates.{module_name}"
    )
    assert module is not None


def test_templates_public_exports_exist():
    templates = importlib.import_module("pylage_layout.templates")

    for name in PUBLIC_TEMPLATES:
        assert hasattr(
            templates, name
        ), f"templates missing public export: {name}"


def test_templates_all_matches_public_api():
    templates = importlib.import_module("pylage_layout.templates")

    assert set(templates.__all__) == set(PUBLIC_TEMPLATES)


def test_templates_are_callable():
    templates = importlib.import_module("pylage_layout.templates")

    for name in PUBLIC_TEMPLATES:
        template = getattr(templates, name)

        assert callable(template), (
            f"templates.{name} must be callable"
        )


def test_templates_return_pylage_components():
    templates = importlib.import_module("pylage_layout.templates")

    for name in PUBLIC_TEMPLATES:
        template = getattr(templates, name)
        component = template()

        assert component is not None, (
            f"{name} returned None"
        )

        assert hasattr(component, "type"), (
            f"{name} must return a PyLage component"
        )
