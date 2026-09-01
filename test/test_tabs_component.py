from pylage import Tabs, Text, Button
from pylage.core.renderer import render


def test_tabs_renders():
    tabs = Tabs(
        Text("Home"),
        Button("Profile"),
    )

    html = render(tabs)

    assert "<div" in html
    assert "Home" in html
    assert "Profile" in html


def test_tabs_supports_props():
    tabs = Tabs(
        class_name="main-tabs",
        title="Sections",
    )

    html = render(tabs)

    assert 'class="main-tabs"' in html
    assert 'title="Sections"' in html


def test_tabs_is_exported():
    assert callable(Tabs)
