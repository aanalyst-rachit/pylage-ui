from pylage import Select, Option
from pylage.core.renderer import render


def test_option_renders_value_and_text():
    html = render(
        Select(
            Option("India", value="india"),
            Option("Japan", value="japan"),
        )
    )

    assert '<option' in html
    assert 'value="india"' in html
    assert ">India</option>" in html
    assert 'value="japan"' in html
    assert ">Japan</option>" in html


def test_option_text_is_not_forwarded_as_html_attribute():
    html = render(
        Select(
            Option("India", value="india"),
        )
    )

    assert 'text="India"' not in html
    assert ">India</option>" in html


def test_select_supports_value():
    html = render(
        Select(
            Option("India", value="india"),
            value="india",
        )
    )

    assert '<select' in html
    assert 'value="india"' in html


def test_select_supports_multiple():
    html = render(
        Select(
            Option("India", value="india"),
            multiple=True,
        )
    )

    assert 'multiple' in html


def test_option_supports_additional_props():
    html = render(
        Select(
            Option(
                "India",
                value="india",
                title="Country",
            )
        )
    )

    assert 'value="india"' in html
    assert 'title="Country"' in html


def test_select_option_order_is_preserved():
    html = render(
        Select(
            Option("India", value="india"),
            Option("Japan", value="japan"),
            Option("Nepal", value="nepal"),
        )
    )

    assert html.index(">India</option>") < html.index(">Japan</option>")
    assert html.index(">Japan</option>") < html.index(">Nepal</option>")
