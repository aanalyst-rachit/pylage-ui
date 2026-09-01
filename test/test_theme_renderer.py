import pylage as ps

from pylage.core.renderer import HTMLRenderer


def test_renderer_can_render_with_theme_css_variables():
    theme = ps.Theme(
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
        spacing={
            "md": "16px",
        },
    )

    renderer = HTMLRenderer(theme=theme)

    html = renderer.render(
        ps.Text(
            "Hello",
            style=ps.Style(
                color="var(--color-primary)",
                background_color="var(--color-background)",
                padding="var(--spacing-md)",
            ),
        )
    )

    assert "--color-primary:#2563eb" in html
    assert "--color-background:#ffffff" in html
    assert "--spacing-md:16px" in html

    assert "color:var(--color-primary)" in html
    assert "background-color:var(--color-background)" in html
    assert "padding:var(--spacing-md)" in html


def test_renderer_without_theme_remains_compatible():
    renderer = HTMLRenderer()

    html = renderer.render(
        ps.Text(
            "Hello",
            style=ps.Style(color="red"),
        )
    )

    assert "color:red" in html


def test_theme_css_is_emitted_once():
    theme = ps.Theme(
        colors={
            "primary": "#2563eb",
        },
    )

    renderer = HTMLRenderer(theme=theme)

    html = renderer.render(
        ps.Column(
            ps.Text("One"),
            ps.Text("Two"),
        )
    )

    assert html.count("--color-primary:#2563eb") == 1
