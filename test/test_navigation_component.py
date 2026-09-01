from pylage import Navigation, Text, Button
from pylage.core.renderer import render


def test_navigation_renders():
    nav = Navigation(
        Text("Home"),
        Button("Login"),
    )

    html = render(nav)

    assert "<nav" in html
    assert "Home" in html
    assert "Login" in html


def test_navigation_supports_props():
    nav = Navigation(
        class_name="main-nav",
        title="Main Navigation",
    )

    html = render(nav)

    assert 'class="main-nav"' in html
    assert 'title="Main Navigation"' in html


def test_navigation_is_exported():
    assert callable(Navigation)
