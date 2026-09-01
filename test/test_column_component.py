from pylage import Column, Text, Button
from pylage.core.renderer import render


def test_column_renders_as_div():
    column = Column(
        Text("Hello"),
        Button(text="Click"),
    )

    html = render(column)

    assert "<div" in html
    assert "Hello" in html
    assert "Click" in html


def test_column_supports_props():
    column = Column(
        class_name="main-column",
        title="Main content",
    )

    html = render(column)

    assert 'class="main-column"' in html
    assert 'title="Main content"' in html
