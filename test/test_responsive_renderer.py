import pylage as ps

from pylage.core.renderer import HTMLRenderer


def test_renderer_can_render_responsive_style():
    responsive = ps.ResponsiveStyle(
        base=ps.Style(
            color="black",
            font_size="16px",
        ),
        sm=ps.Style(
            color="blue",
        ),
        md=ps.Style(
            color="green",
            font_size="20px",
        ),
    )

    renderer = HTMLRenderer()

    html = renderer.render(
        ps.Text(
            "Hello",
            style=responsive,
        )
    )

    assert "color:black" in html
    assert "font-size:16px" in html
    assert "@media" in html
    assert "color:blue" in html
    assert "color:green" in html
    assert "font-size:20px" in html


def test_renderer_without_responsive_style_remains_compatible():
    renderer = HTMLRenderer()

    html = renderer.render(
        ps.Text(
            "Hello",
            style=ps.Style(color="red"),
        )
    )

    assert "color:red" in html
    assert "@media" not in html


def test_responsive_style_can_use_theme_variables_in_renderer():
    theme = ps.Theme(
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
    )

    responsive = ps.ResponsiveStyle(
        base=ps.Style(
            color="var(--color-primary)",
        ),
        md=ps.Style(
            color="var(--color-background)",
        ),
    )

    renderer = HTMLRenderer(theme=theme)

    html = renderer.render(
        ps.Text(
            "Hello",
            style=responsive,
        )
    )

    assert "--color-primary:#2563eb" in html
    assert "--color-background:#ffffff" in html
    assert "var(--color-primary)" in html
    assert "var(--color-background)" in html
    assert "@media" in html
