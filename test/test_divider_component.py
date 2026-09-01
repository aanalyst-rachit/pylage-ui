from pylage import Divider
from pylage.core.renderer import render


def test_divider_creates_divider_component():
    divider = Divider()

    assert divider.type == "Divider"


def test_divider_renders_as_hr():
    divider = Divider()

    html = render(divider)

    assert html.startswith("<hr ")
    assert "</hr>" not in html


def test_divider_supports_props():
    divider = Divider(
        class_name="section-divider",
        title="Section divider",
    )

    html = render(divider)

    assert 'class="section-divider"' in html
    assert 'title="Section divider"' in html
