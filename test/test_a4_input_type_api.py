import pytest

import pylage as ps
from pylage.core.renderer import render


@pytest.mark.parametrize(
    ("input_type", "expected"),
    [
        ("text", 'type="text"'),
        ("checkbox", 'type="checkbox"'),
        ("radio", 'type="radio"'),
        ("date", 'type="date"'),
        ("range", 'type="range"'),
    ],
)
def test_input_supports_input_type(input_type, expected):
    html = render(ps.Input(input_type=input_type))

    assert "<input" in html
    assert expected in html
    assert "input_type=" not in html


def test_input_defaults_without_input_type():
    html = render(ps.Input())

    assert "<input" in html
    assert 'type="' not in html


def test_input_type_does_not_collide_with_component_type():
    input_box = ps.Input(input_type="checkbox")

    assert input_box.type == "Input"
    assert input_box.props["_html_type"] == "checkbox"


def test_input_preserves_existing_props():
    html = render(
        ps.Input(
            value="Dollar",
            input_type="text",
            disabled=True,
            title="Name",
        )
    )

    assert 'value="Dollar"' in html
    assert 'type="text"' in html
    assert "disabled" in html
    assert 'title="Name"' in html


def test_input_type_is_not_forwarded_as_raw_html_attribute():
    html = render(ps.Input(input_type="date"))

    assert "input_type=" not in html
    assert 'type="date"' in html
