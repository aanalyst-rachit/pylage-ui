from pylage import Popover, Text, Button
from pylage.core.renderer import render


def test_popover_renders_as_div():
    popover = Popover(
        Text("Popover content"),
    )

    html = render(popover)

    assert "<div" in html


def test_popover_supports_props():
    popover = Popover(
        class_name="popover",
        title="Additional information",
    )

    html = render(popover)

    assert 'class="popover"' in html
    assert 'title="Additional information"' in html


def test_popover_renders_children():
    popover = Popover(
        Text("Details"),
        Button(text="Close"),
    )

    html = render(popover)

    assert "Details" in html
    assert "Close" in html
