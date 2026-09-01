from pylage import Switch
from pylage.core.renderer import render


def test_switch_renders_as_checkbox():
    switch = Switch()

    html = render(switch)

    assert "<input" in html
    assert 'type="checkbox"' in html


def test_switch_supports_props():
    switch = Switch(
        class_name="dark-switch",
        title="Enable notifications",
    )

    html = render(switch)

    assert 'class="dark-switch"' in html
    assert 'title="Enable notifications"' in html


def test_switch_supports_checked():
    switch = Switch(checked=True)

    html = render(switch)

    assert "checked" in html
