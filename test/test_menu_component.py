from pylage import Menu, Text, Button
from pylage.core.renderer import render


def test_menu_renders_as_menu():
    menu = Menu(
        Text("Home"),
        Text("Settings"),
        Text("Logout"),
    )

    html = render(menu)

    assert "<menu" in html


def test_menu_supports_props():
    menu = Menu(
        class_name="main-menu",
        title="Main menu",
    )

    html = render(menu)

    assert 'class="main-menu"' in html
    assert 'title="Main menu"' in html


def test_menu_renders_children():
    menu = Menu(
        Button(text="Home"),
        Text("Settings"),
        Button(text="Logout"),
    )

    html = render(menu)

    assert "Home" in html
    assert "Settings" in html
    assert "Logout" in html
