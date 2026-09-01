from pylage import Drawer, Text, Button
from pylage.core.renderer import render


def test_drawer_renders_as_aside():
    drawer = Drawer(
        Text("Navigation"),
        Button(text="Home"),
    )

    html = render(drawer)

    assert "<aside" in html


def test_drawer_supports_props():
    drawer = Drawer(
        class_name="sidebar",
        title="Navigation drawer",
    )

    html = render(drawer)

    assert 'class="sidebar"' in html
    assert 'title="Navigation drawer"' in html


def test_drawer_renders_children():
    drawer = Drawer(
        Text("Dashboard"),
        Button(text="Settings"),
    )

    html = render(drawer)

    assert "Dashboard" in html
    assert "Settings" in html
