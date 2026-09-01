from pylage.core.component import Component
from pylage.core.registry import registry
from pylage.core.renderer import HTMLRenderer
from pylage.core.state import State

print("=== PYLAGE REGISTRY RENDER METADATA TEST ===")

renderer = HTMLRenderer()

component = Component(
    type="Button",
    props={
        "text": State("Save"),
        "value": State("123"),
        "disabled": State(True),
        "title": State("Save button"),
    },
)

html = renderer.render(component)

print("Rendered HTML:")
print(html)

# Component identity must be present.
assert f'data-pylage-id="{component.id}"' in html

# Registry-driven props must reach the rendered DOM.
assert "Save" in html
assert 'value="123"' in html
assert "disabled" in html
assert 'title="Save button"' in html

print("Registry-driven HTML rendering: PASS")

# Verify registry metadata used by the Button contract.
definition = registry.require("Button")

assert definition.props is not None

assert definition.props["text"].kind == "text"
assert definition.props["value"].kind == "attribute"
assert definition.props["value"].html_name == "value"
assert definition.props["disabled"].kind == "boolean"
assert definition.props["disabled"].html_name == "disabled"
assert definition.props["title"].kind == "attribute"
assert definition.props["title"].html_name == "title"

print("Registry prop metadata: PASS")

print()
print("=== REGISTRY RENDER METADATA TEST PASS ===")
