from pylage import Tooltip, Text, Button
from pylage.core.renderer import render


def test_tooltip_renders_as_span():
    tooltip = Tooltip(
        Text("Hover me"),
    )

    html = render(tooltip)

    assert "<span" in html


def test_tooltip_supports_props():
    tooltip = Tooltip(
        class_name="tooltip",
        title="Helpful information",
    )

    html = render(tooltip)

    assert 'class="tooltip"' in html
    assert 'title="Helpful information"' in html


def test_tooltip_renders_children():
    tooltip = Tooltip(
        Text("Info"),
        Button(text="Action"),
    )

    html = render(tooltip)

    assert "Info" in html
    assert "Action" in html
