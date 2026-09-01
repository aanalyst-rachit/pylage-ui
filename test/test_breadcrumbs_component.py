from pylage import Breadcrumbs, Text, Button
from pylage.core.renderer import render


def test_breadcrumbs_renders_as_nav():
    breadcrumbs = Breadcrumbs(
        Text("Home"),
        Text("Products"),
        Text("Details"),
    )

    html = render(breadcrumbs)

    assert "<nav" in html


def test_breadcrumbs_supports_props():
    breadcrumbs = Breadcrumbs(
        class_name="breadcrumbs",
        title="Page navigation",
    )

    html = render(breadcrumbs)

    assert 'class="breadcrumbs"' in html
    assert 'title="Page navigation"' in html


def test_breadcrumbs_renders_children():
    breadcrumbs = Breadcrumbs(
        Text("Home"),
        Button(text="Products"),
    )

    html = render(breadcrumbs)

    assert "Home" in html
    assert "Products" in html
