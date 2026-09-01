from pylage import Table, Text
from pylage.core.renderer import render


def test_table_renders_as_table():
    table = Table()

    html = render(table)

    assert "<table" in html
    assert "</table>" in html


def test_table_renders_children():
    table = Table(
        Text("Row 1"),
        Text("Row 2"),
    )

    html = render(table)

    assert "Row 1" in html
    assert "Row 2" in html


def test_table_supports_props():
    table = Table(
        class_name="data-table",
        title="Users",
    )

    html = render(table)

    assert 'class="data-table"' in html
    assert 'title="Users"' in html
