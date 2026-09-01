import pylage as ps
from pylage.core.renderer import render


def test_row_registry_props_render():
    html = render(
        ps.Row(
            ps.Text("A"),
            class_name="main-row",
            title="Row title",
        )
    )

    assert 'class="main-row"' in html
    assert 'title="Row title"' in html
    assert "A" in html


def test_column_registry_props_render():
    html = render(
        ps.Column(
            ps.Text("A"),
            class_name="main-column",
            title="Column title",
        )
    )

    assert 'class="main-column"' in html
    assert 'title="Column title"' in html
    assert "A" in html


def test_grid_registry_props_render():
    html = render(
        ps.Grid(
            ps.Text("A"),
            class_name="main-grid",
            title="Grid title",
        )
    )

    assert 'class="main-grid"' in html
    assert 'title="Grid title"' in html
    assert "A" in html


def test_nested_layout_props_are_isolated():
    html = render(
        ps.Column(
            ps.Row(
                ps.Text("A"),
                class_name="inner-row",
            ),
            ps.Grid(
                ps.Text("B"),
                class_name="inner-grid",
            ),
            class_name="outer-column",
        )
    )

    assert 'class="outer-column"' in html
    assert 'class="inner-row"' in html
    assert 'class="inner-grid"' in html
    assert html.count('class="') == 3


def test_layout_state_style_values_are_resolved():
    width = ps.State("90%")
    gap = ps.State("20px")

    html = render(
        ps.Row(
            ps.Text("State"),
            style=ps.Style(
                width=width,
                gap=gap,
            ),
        )
    )

    assert "width:90%" in html
    assert "gap:20px" in html
    assert "State(&#x27;90%&#x27;)" not in html
    assert "State(&#x27;20px&#x27;)" not in html
