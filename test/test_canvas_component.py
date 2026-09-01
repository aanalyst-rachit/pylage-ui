from pylage import Canvas
from pylage.core.renderer import render


def test_canvas_creates_canvas_component():
    canvas = Canvas()

    assert canvas.type == "Canvas"


def test_canvas_renders_as_svg_container():
    canvas = Canvas(
        width=400,
        height=300,
    )

    html = render(canvas)

    assert "<svg" in html
    assert 'width="400"' in html
    assert 'height="300"' in html
    assert "</svg>" in html


def test_canvas_supports_props():
    canvas = Canvas(
        width=800,
        height=600,
        class_name="drawing-area",
        title="Drawing Canvas",
    )

    html = render(canvas)

    assert 'width="800"' in html
    assert 'height="600"' in html
    assert 'class="drawing-area"' in html
    assert 'title="Drawing Canvas"' in html
