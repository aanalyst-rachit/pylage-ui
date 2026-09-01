import pylage as ps


def test_style_supports_layout_constraints():
    style = ps.Style(
        width="100%",
        min_width="320px",
        max_width="1200px",
        height="auto",
        min_height="100px",
        max_height="800px",
    )

    css = style.to_css()

    assert "width:100%" in css
    assert "min-width:320px" in css
    assert "max-width:1200px" in css
    assert "height:auto" in css
    assert "min-height:100px" in css
    assert "max-height:800px" in css


def test_style_supports_flex_layout_constraints():
    style = ps.Style(
        display="flex",
        flex_direction="column",
        flex_wrap="wrap",
        flex_grow=1,
        flex_shrink=0,
        flex_basis="200px",
        gap="16px",
        row_gap="8px",
        column_gap="12px",
    )

    css = style.to_css()

    assert "display:flex" in css
    assert "flex-direction:column" in css
    assert "flex-wrap:wrap" in css
    assert "flex-grow:1" in css
    assert "flex-shrink:0" in css
    assert "flex-basis:200px" in css
    assert "gap:16px" in css
    assert "row-gap:8px" in css
    assert "column-gap:12px" in css


def test_style_supports_grid_layout_constraints():
    style = ps.Style(
        display="grid",
        grid_template_columns="repeat(3, 1fr)",
        grid_template_rows="auto",
        grid_column="1 / 3",
        grid_row="1",
    )

    css = style.to_css()

    assert "display:grid" in css
    assert "grid-template-columns:repeat(3, 1fr)" in css
    assert "grid-template-rows:auto" in css
    assert "grid-column:1 / 3" in css
    assert "grid-row:1" in css


def test_column_can_override_default_layout_style():
    column = ps.Column(
        ps.Text("Hello"),
        style=ps.Style(
            width="100%",
            max_width="600px",
            gap="16px",
        ),
    )

    from pylage.core.renderer import render

    html = render(column)

    assert "display:flex" in html
    assert "flex-direction:column" in html
    assert "width:100%" in html
    assert "max-width:600px" in html
    assert "gap:16px" in html


def test_layout_constraints_work_with_theme_variables():
    theme = ps.Theme(
        spacing={
            "md": "16px",
        },
    )

    style = ps.Style(
        width="100%",
        max_width="var(--spacing-md)",
        gap="var(--spacing-md)",
    )

    css = style.to_css()

    assert "width:100%" in css
    assert "max-width:var(--spacing-md)" in css
    assert "gap:var(--spacing-md)" in css

    assert "--spacing-md:16px" in theme.to_css()
