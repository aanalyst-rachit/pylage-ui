from pylage import Spinner
from pylage.core.renderer import render


def test_spinner_renders_as_div():
    spinner = Spinner()

    html = render(spinner)

    assert "<div" in html


def test_spinner_supports_props():
    spinner = Spinner(
        class_name="loading-spinner",
        title="Loading",
    )

    html = render(spinner)

    assert 'class="loading-spinner"' in html
    assert 'title="Loading"' in html


def test_spinner_supports_text():
    spinner = Spinner(
        text="Please wait",
    )

    html = render(spinner)

    assert "Please wait" in html
