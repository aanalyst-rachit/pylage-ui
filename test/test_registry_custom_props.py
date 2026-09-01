from pylage.core.component import Component
from pylage.core.registry import PropDefinition, registry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE CUSTOM REGISTRY PROP RENDERING TEST ===")


registry.register(
    "Card",
    "section",
    props={
        "label": PropDefinition(
            "label",
            kind="text",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "hidden": PropDefinition(
            "hidden",
            kind="boolean",
            html_name="hidden",
        ),
        "data_id": PropDefinition(
            "data_id",
            kind="attribute",
            html_name="data-id",
        ),
    },
)


# ---------------------------------------------------------
# Registry-defined text prop
# ---------------------------------------------------------
card = Component(
    type="Card",
    props={
        "label": "Hello Card",
        "class_name": "premium-card",
        "hidden": True,
        "data_id": "card-01",
    },
)

html = HTMLRenderer().render(card)

print(html)

assert "<section" in html
assert "Hello Card" in html
assert 'class="premium-card"' in html
assert "hidden" in html
assert 'data-id="card-01"' in html

# Text props must NOT become HTML attributes.
assert 'label="Hello Card"' not in html

print("Registry text props: PASS")
print("Registry HTML names: PASS")
print("Registry boolean props: PASS")
print("Registry custom attributes: PASS")


# ---------------------------------------------------------
# Text prop + children
# ---------------------------------------------------------
card_with_children = Component(
    type="Card",
    props={
        "label": "Title",
    },
    children=[
        Component(
            type="Heading",
            props={"text": "Child"},
        )
    ],
)

html = HTMLRenderer().render(card_with_children)

print(html)

assert "Title" in html
assert "<h1" in html
assert "Child" in html
assert 'label="Title"' not in html

print("Text prop + children: PASS")


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------
registry.register(
    "Card",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

print()
print("=== CUSTOM REGISTRY PROP RENDERING PASS ===")
