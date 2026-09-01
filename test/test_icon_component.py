from pylage import Icon
from pylage.core.renderer import render


def test_icon_creates_icon_component():
    icon = Icon()

    assert icon.type == "Icon"


def test_icon_renders_as_icon_container():
    icon = Icon(
        name="home",
    )

    html = render(icon)

    assert "home" in html
    assert "<span" in html


def test_icon_supports_props():
    icon = Icon(
        name="settings",
        class_name="app-icon",
        title="Settings",
    )

    html = render(icon)

    assert "settings" in html
    assert 'class="app-icon"' in html
    assert 'title="Settings"' in html
