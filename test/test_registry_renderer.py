import pylage as ps

from pylage.core.component import Component
from pylage.core.registry import registry
from pylage.core.renderer import render


def test_registry_renderer():
    print("=== PYLAGE REGISTRY RENDERER TEST ===")

    # Built-in component
    heading = ps.Heading("Hello")

    html = render(heading)

    print(html)

    assert "<h1" in html
    assert "Hello" in html
    assert 'data-pylage-id="' in html

    print("Built-in registry rendering: PASS")

    # Custom component through registry
    registry.register("Card", "section")

    card = Component(
        type="Card",
        props={"text": "Hello Card"},
    )

    html = render(card)

    print(html)

    assert "<section" in html
    assert "Hello Card" in html

    print("Custom registry rendering: PASS")

    # Custom renderer
    def render_card(renderer, component):
        text = renderer._value(
            component.props.get("text", "")
        )

        return (
            f'<article data-pylage-id="{component.id}">'
            f"{text}"
            f"</article>"
        )

    registry.register(
        "CustomCard",
        "article",
        renderer=render_card,
    )

    custom = Component(
        type="CustomCard",
        props={"text": "Custom"},
    )

    html = render(custom)

    print(html)

    assert "<article" in html
    assert "Custom" in html

    print("Custom renderer dispatch: PASS")

    print()
    print("=== REGISTRY RENDERER PASS ===")
