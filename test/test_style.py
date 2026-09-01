import pytest

from pylage import Style


def test_style_can_be_created():
    style = Style(
        color="red",
        font_size="20px",
    )

    assert style.color == "red"
    assert style.font_size == "20px"


def test_style_generates_css():
    style = Style(
        color="red",
        font_size="20px",
        margin="10px",
    )

    assert style.to_css() == (
        "color:red;"
        "font-size:20px;"
        "margin:10px"
    )


def test_style_uses_kebab_case():
    style = Style(
        background_color="black",
        margin_top="10px",
        justify_content="center",
    )

    assert style.to_css() == (
        "background-color:black;"
        "margin-top:10px;"
        "justify-content:center"
    )


def test_style_is_immutable():
    style = Style(color="red")

    with pytest.raises(AttributeError):
        style.color = "blue"


def test_style_renders_on_component():
    import pylage as ps

    component = ps.Text(
        "Hello",
        style=ps.Style(
            color="red",
            font_size="20px",
        ),
    )

    html = ps.core.renderer.render(component) if hasattr(ps, "core") else None

    # Use the public renderer directly.
    from pylage.core.renderer import render

    html = render(component)

    assert 'style="color:red;font-size:20px"' in html


def test_style_renders_with_html_escaping():
    from pylage import Text, Style
    from pylage.core.renderer import render

    component = Text(
        "Hello",
        style=Style(
            color='red"blue',
        ),
    )

    html = render(component)

    assert 'style="color:red&quot;blue"' in html


def test_component_without_style_has_no_style_attribute():
    from pylage import Text
    from pylage.core.renderer import render

    html = render(Text("Hello"))

    assert " style=" not in html


def test_style_merge_user_values_override_defaults():
    from pylage import Style

    default = Style(
        display="flex",
        flex_direction="column",
        gap="5px",
    )

    override = Style(
        display="grid",
        gap="20px",
    )

    merged = default.merge(override)

    assert merged.display == "grid"
    assert merged.flex_direction == "column"
    assert merged.gap == "20px"


def test_style_merge_does_not_mutate_original():
    from pylage import Style

    default = Style(display="flex")
    override = Style(display="grid")

    merged = default.merge(override)

    assert default.display == "flex"
    assert override.display == "grid"
    assert merged.display == "grid"


def test_column_uses_default_style():
    from pylage import Column, Text
    from pylage.core.renderer import render

    html = render(
        Column(Text("Hello"))
    )

    assert 'style="display:flex;flex-direction:column"' in html


def test_column_user_style_overrides_default():
    from pylage import Column, Style, Text
    from pylage.core.renderer import render

    html = render(
        Column(
            Text("Hello"),
            style=Style(
                display="grid",
                gap="10px",
            ),
        )
    )

    assert 'style="display:grid;flex-direction:column;gap:10px"' in html
    assert 'style="display:flex;flex-direction:column;"' not in html


def test_style_supports_custom_css_properties():
    from pylage import Style

    style = Style(
        color="var(--primary-color)",
        custom={
            "--primary-color": "#2563eb",
        },
    )

    assert style.to_css() == (
        "color:var(--primary-color);"
        "--primary-color:#2563eb"
    )


def test_custom_css_properties_merge():
    from pylage import Style

    default = Style(
        custom={
            "--primary-color": "blue",
            "--spacing": "8px",
        }
    )

    override = Style(
        custom={
            "--primary-color": "red",
            "--radius": "6px",
        }
    )

    merged = default.merge(override)

    assert merged.custom == {
        "--primary-color": "red",
        "--spacing": "8px",
        "--radius": "6px",
    }


def test_invalid_custom_css_property_name_is_rejected():
    from pylage import Style

    style = Style(
        custom={
            "primary-color": "red",
        }
    )

    try:
        style.to_css()
    except ValueError as exc:
        assert "must start with '--'" in str(exc)
    else:
        raise AssertionError(
            "Invalid custom CSS property name was accepted"
        )


def test_none_custom_css_values_are_ignored():
    from pylage import Style

    style = Style(
        custom={
            "--primary-color": "#2563eb",
            "--unused": None,
        }
    )

    assert style.to_css() == (
        "--primary-color:#2563eb"
    )


def test_style_custom_properties_render_to_html():
    from pylage import Text, Style
    from pylage.core.renderer import render

    html = render(
        Text(
            "Hello",
            style=Style(
                color="var(--primary-color)",
                custom={
                    "--primary-color": "#2563eb",
                },
            ),
        )
    )

    assert (
        'style="color:var(--primary-color);'
        '--primary-color:#2563eb"'
    ) in html
