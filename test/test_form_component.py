from pylage import Form, Input, Button
from pylage.core.renderer import render


def test_form_renders_as_form():
    form = Form(
        Input(),
        Button("Submit"),
    )

    html = render(form)

    assert "<form" in html
    assert "</form>" in html


def test_form_renders_children():
    form = Form(
        Input(),
        Button("Submit"),
    )

    html = render(form)

    assert "<input" in html
    assert "<button" in html
    assert "Submit" in html


def test_form_supports_props():
    form = Form(
        method="post",
        action="/submit",
    )

    html = render(form)

    assert 'method="post"' in html
    assert 'action="/submit"' in html
