import pylage as ps


def test_responsive_style_can_be_created():
    responsive = ps.ResponsiveStyle(
        base=ps.Style(color="black"),
        sm=ps.Style(color="blue"),
        md=ps.Style(color="green"),
    )

    assert responsive.base.color == "black"
    assert responsive.sm.color == "blue"
    assert responsive.md.color == "green"


def test_responsive_style_generates_media_queries():
    responsive = ps.ResponsiveStyle(
        base=ps.Style(font_size="16px"),
        sm=ps.Style(font_size="18px"),
        md=ps.Style(font_size="20px"),
    )

    css = responsive.to_css()

    assert "font-size:16px" in css
    assert "@media" in css
    assert "font-size:18px" in css
    assert "font-size:20px" in css


def test_responsive_style_can_use_theme_variables():
    responsive = ps.ResponsiveStyle(
        base=ps.Style(
            color="var(--color-primary)",
        ),
        md=ps.Style(
            color="var(--color-background)",
        ),
    )

    css = responsive.to_css()

    assert "color:var(--color-primary)" in css
    assert "color:var(--color-background)" in css


def test_responsive_style_is_immutable():
    responsive = ps.ResponsiveStyle(
        base=ps.Style(color="black"),
    )

    try:
        responsive.base = ps.Style(color="red")
    except Exception:
        pass
    else:
        raise AssertionError(
            "ResponsiveStyle must be immutable"
        )


def test_empty_responsive_style_generates_empty_css():
    responsive = ps.ResponsiveStyle()

    assert responsive.to_css() == ""
