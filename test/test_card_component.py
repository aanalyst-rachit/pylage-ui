from pylage import Card, Text
from pylage.core.renderer import render


def test_card_creates_card_component():
    card = Card()

    assert card.type == "Card"


def test_card_supports_children():
    card = Card(
        Text("Hello"),
    )

    html = render(card)

    assert "Hello" in html


def test_card_supports_props():
    card = Card(
        class_name="premium-card",
        title="Premium",
    )

    html = render(card)

    assert 'class="premium-card"' in html
    assert 'title="Premium"' in html
