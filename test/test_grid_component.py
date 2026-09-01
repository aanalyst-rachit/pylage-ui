from pylage import Grid, Text, Button
from pylage.core.renderer import render


def test_grid_creates_grid_component():
    grid = Grid()

    assert grid.type == "Grid"


def test_grid_supports_children():
    grid = Grid(
        Text("Item 1"),
        Button("Item 2"),
    )

    html = render(grid)

    assert "Item 1" in html
    assert "Item 2" in html


def test_grid_supports_props():
    grid = Grid(
        class_name="main-grid",
        title="Dashboard",
    )

    html = render(grid)

    assert 'class="main-grid"' in html
    assert 'title="Dashboard"' in html
