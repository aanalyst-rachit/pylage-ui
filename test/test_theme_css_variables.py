import pylage as ps


def test_theme_css_variables_can_be_used_by_style():
    theme = ps.Theme(
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
        spacing={
            "md": "16px",
        },
    )

    style = ps.Style(
        color="var(--color-primary)",
        background_color="var(--color-background)",
        padding="var(--spacing-md)",
    )

    assert style.to_css() == (
        "color:var(--color-primary);"
        "background-color:var(--color-background);"
        "padding:var(--spacing-md)"
    )

    css = theme.to_css()

    assert "--color-primary:#2563eb" in css
    assert "--color-background:#ffffff" in css
    assert "--spacing-md:16px" in css


def test_theme_css_can_be_combined_with_component_style():
    theme = ps.Theme(
        colors={
            "primary": "#2563eb",
        },
        spacing={
            "md": "16px",
        },
    )

    style = ps.Style(
        color="var(--color-primary)",
        padding="var(--spacing-md)",
    )

    from pylage import Text
    from pylage.core.renderer import render

    html = render(
        Text(
            "Hello",
            style=style,
        )
    )

    assert "color:var(--color-primary)" in html
    assert "padding:var(--spacing-md)" in html

    assert "--color-primary:#2563eb" in theme.to_css()
    assert "--spacing-md:16px" in theme.to_css()


def test_theme_css_variable_names_are_stable():
    theme = ps.Theme(
        colors={
            "primary_text": "#111827",
        },
        spacing={
            "extra_large": "32px",
        },
        radius={
            "extra_large": "16px",
        },
    )

    css = theme.to_css()

    assert "--color-primary-text:#111827" in css
    assert "--spacing-extra-large:32px" in css
    assert "--radius-extra-large:16px" in css
