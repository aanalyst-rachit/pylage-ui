from pylage import Slider
from pylage.core.renderer import render


def test_slider_renders_as_range():
    slider = Slider()

    html = render(slider)

    assert "<input" in html
    assert 'type="range"' in html


def test_slider_supports_props():
    slider = Slider(
        class_name="volume-slider",
        title="Volume",
    )

    html = render(slider)

    assert 'class="volume-slider"' in html
    assert 'title="Volume"' in html


def test_slider_supports_value():
    slider = Slider(value=50)

    html = render(slider)

    assert 'value="50"' in html
