from pylage import Toast
from pylage.core.renderer import render


def test_toast_renders_as_div():
    toast = Toast()

    html = render(toast)

    assert "<div" in html


def test_toast_supports_props():
    toast = Toast(
        class_name="success-toast",
        title="Success",
    )

    html = render(toast)

    assert 'class="success-toast"' in html
    assert 'title="Success"' in html


def test_toast_supports_text():
    toast = Toast(
        text="Saved successfully",
    )

    html = render(toast)

    assert "Saved successfully" in html
