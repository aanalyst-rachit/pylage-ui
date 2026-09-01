from pylage import Select, Text, Button
from pylage.core.renderer import render


def test_select_renders_as_select():
    select = Select()

    html = render(select)

    assert "<select" in html
    assert "</select>" in html


def test_select_renders_children():
    select = Select(
        Text("Option A"),
        Button("Option B"),
    )

    html = render(select)

    assert "Option A" in html
    assert "Option B" in html


def test_select_supports_props():
    select = Select(
        class_name="country-select",
        title="Choose country",
    )

    html = render(select)

    assert 'class="country-select"' in html
    assert 'title="Choose country"' in html
