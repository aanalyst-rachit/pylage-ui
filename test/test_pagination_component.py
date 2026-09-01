from pylage import Pagination, Text, Button
from pylage.core.renderer import render


def test_pagination_renders_as_nav():
    pagination = Pagination(
        Text("1"),
        Text("2"),
        Text("3"),
    )

    html = render(pagination)

    assert "<nav" in html


def test_pagination_supports_props():
    pagination = Pagination(
        class_name="pagination",
        title="Page navigation",
    )

    html = render(pagination)

    assert 'class="pagination"' in html
    assert 'title="Page navigation"' in html


def test_pagination_renders_children():
    pagination = Pagination(
        Button(text="Previous"),
        Text("2"),
        Button(text="Next"),
    )

    html = render(pagination)

    assert "Previous" in html
    assert "2" in html
    assert "Next" in html
