from pylage import Checkbox
from pylage.core.renderer import render


def test_checkbox_renders_as_checkbox():
    checkbox = Checkbox()

    html = render(checkbox)

    assert "<input" in html
    assert 'type="checkbox"' in html


def test_checkbox_supports_props():
    checkbox = Checkbox(
        class_name="agree",
        title="Accept terms",
    )

    html = render(checkbox)

    assert 'class="agree"' in html
    assert 'title="Accept terms"' in html


def test_checkbox_supports_checked():
    checkbox = Checkbox(checked=True)

    html = render(checkbox)

    assert "checked" in html
