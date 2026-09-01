from pylage import Accordion, Text, Button
from pylage.core.renderer import render


def test_accordion_creates_accordion_component():
    accordion = Accordion()

    assert accordion.type == "Accordion"


def test_accordion_supports_children():
    accordion = Accordion(
        Text("Content"),
        Button("Action"),
    )

    html = render(accordion)

    assert "Content" in html
    assert "Action" in html


def test_accordion_supports_props():
    accordion = Accordion(
        class_name="faq-accordion",
        title="FAQ",
    )

    html = render(accordion)

    assert 'class="faq-accordion"' in html
    assert 'title="FAQ"' in html
