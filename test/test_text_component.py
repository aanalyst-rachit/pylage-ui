from pylage import Text
from pylage.core.renderer import render


def test_text_creates_text_component():
    text = Text("Hello PyLage")

    assert text.type == "Text"
    assert text.props["text"] == "Hello PyLage"


def test_text_renders_as_plain_text():
    text = Text("Hello PyLage")

    html = render(text)

    assert "Hello PyLage" in html
    assert "<div" in html


def test_text_escapes_html():
    text = Text("<script>alert(1)</script>")

    html = render(text)

    assert "&lt;script&gt;" in html
    assert "<script>" not in html


def test_text_supports_state():
    from pylage import State

    state = State("Initial")
    text = Text(state)

    assert text.props["text"] is state
    assert "Initial" in render(text)
