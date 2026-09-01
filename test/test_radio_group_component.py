from pylage import RadioGroup, Text, Button
from pylage.core.renderer import render


def test_radio_group_renders_as_container():
    group = RadioGroup()

    html = render(group)

    assert "<div" in html
    assert "</div>" in html


def test_radio_group_renders_children():
    group = RadioGroup(
        Text("Option A"),
        Button("Option B"),
    )

    html = render(group)

    assert "Option A" in html
    assert "Option B" in html


def test_radio_group_supports_props():
    group = RadioGroup(
        class_name="gender-group",
        title="Choose one",
    )

    html = render(group)

    assert 'class="gender-group"' in html
    assert 'title="Choose one"' in html
