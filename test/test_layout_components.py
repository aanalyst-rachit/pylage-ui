import pylage as ps

from pylage.core.renderer import render


def test_column_is_flex_column_by_default():
    html = render(
        ps.Column(
            ps.Text("One"),
            ps.Text("Two"),
        )
    )

    assert "display:flex" in html
    assert "flex-direction:column" in html
    assert "One" in html
    assert "Two" in html


def test_column_layout_can_be_customized():
    html = render(
        ps.Column(
            ps.Text("One"),
            ps.Text("Two"),
            style=ps.Style(
                flex_direction="row",
                flex_wrap="wrap",
                gap="16px",
                justify_content="space-between",
                align_items="center",
            ),
        )
    )

    assert "display:flex" in html
    assert "flex-direction:row" in html
    assert "flex-wrap:wrap" in html
    assert "gap:16px" in html
    assert "justify-content:space-between" in html
    assert "align-items:center" in html


def test_grid_can_render_grid_layout():
    html = render(
        ps.Grid(
            ps.Text("One"),
            ps.Text("Two"),
            ps.Text("Three"),
            style=ps.Style(
                display="grid",
                grid_template_columns="repeat(3, 1fr)",
                gap="16px",
            ),
        )
    )

    assert "display:grid" in html
    assert "grid-template-columns:repeat(3, 1fr)" in html
    assert "gap:16px" in html
    assert "One" in html
    assert "Two" in html
    assert "Three" in html


def test_layout_constraints_can_be_combined():
    html = render(
        ps.Grid(
            ps.Text("Content"),
            style=ps.Style(
                width="100%",
                min_width="320px",
                max_width="1200px",
                min_height="200px",
                padding="24px",
                margin="auto",
            ),
        )
    )

    assert "width:100%" in html
    assert "min-width:320px" in html
    assert "max-width:1200px" in html
    assert "min-height:200px" in html
    assert "padding:24px" in html
    assert "margin:auto" in html


def test_layout_state_values_are_rendered():
    width = ps.State("80%")
    gap = ps.State("12px")

    html = render(
        ps.Grid(
            ps.Text("State layout"),
            style=ps.Style(
                width=width,
                gap=gap,
            ),
        )
    )

    assert "width:80%" in html
    assert "gap:12px" in html
