import pytest

from pylage import Theme


def test_theme_can_be_created():
    theme = Theme(
        name="light",
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
        spacing={
            "sm": "4px",
            "md": "8px",
        },
        radius={
            "md": "8px",
        },
        fonts={
            "body": "Inter, sans-serif",
        },
    )

    assert theme.name == "light"
    assert theme.color("primary") == "#2563eb"
    assert theme.spacing_value("md") == "8px"
    assert theme.radius_value("md") == "8px"
    assert theme.font("body") == "Inter, sans-serif"


def test_theme_generates_css_variables():
    theme = Theme(
        colors={
            "primary": "#2563eb",
            "background_color": "#ffffff",
        },
        spacing={
            "md": "8px",
        },
        radius={
            "large": "12px",
        },
    )

    assert theme.to_css() == (
        "--color-primary:#2563eb;"
        "--color-background-color:#ffffff;"
        "--spacing-md:8px;"
        "--radius-large:12px"
    )


def test_theme_token_names_use_kebab_case():
    theme = Theme(
        colors={
            "primary_text": "#111827",
        },
        spacing={
            "extra_large": "32px",
        },
    )

    assert theme.to_css() == (
        "--color-primary-text:#111827;"
        "--spacing-extra-large:32px"
    )


def test_theme_is_immutable():
    theme = Theme(
        name="light",
        colors={"primary": "red"},
    )

    with pytest.raises(TypeError):
        theme.colors["primary"] = "blue"

    with pytest.raises(Exception):
        theme.name = "dark"


def test_unknown_color_token_is_rejected():
    theme = Theme(
        colors={"primary": "red"},
    )

    with pytest.raises(KeyError, match="Unknown color token"):
        theme.color("missing")


def test_unknown_spacing_token_is_rejected():
    theme = Theme(
        spacing={"md": "8px"},
    )

    with pytest.raises(KeyError, match="Unknown spacing token"):
        theme.spacing_value("missing")


def test_unknown_radius_token_is_rejected():
    theme = Theme(
        radius={"md": "8px"},
    )

    with pytest.raises(KeyError, match="Unknown radius token"):
        theme.radius_value("missing")


def test_unknown_font_token_is_rejected():
    theme = Theme(
        fonts={"body": "Inter"},
    )

    with pytest.raises(KeyError, match="Unknown font token"):
        theme.font("missing")


def test_none_token_values_are_ignored():
    theme = Theme(
        colors={
            "primary": "#2563eb",
            "secondary": None,
        },
        spacing={
            "md": None,
        },
    )

    assert theme.to_css() == "--color-primary:#2563eb"


def test_empty_theme_generates_empty_css():
    theme = Theme()

    assert theme.to_css() == ""
