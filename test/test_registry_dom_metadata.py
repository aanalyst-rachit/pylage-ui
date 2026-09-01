from pylage.core.component import Component
from pylage.core.registry import ComponentRegistry, PropDefinition
from pylage.core.renderer import HTMLRenderer
from pylage.core.state import State

print("=== PYLAGE REGISTRY DOM METADATA TEST ===")

registry = ComponentRegistry()

registry.register(
    "TestButton",
    "button",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "disabled": PropDefinition(
            "disabled",
            kind="boolean",
            html_name="disabled",
        ),
        "label": PropDefinition(
            "label",
            kind="text",
        ),
    },
)

definition = registry.get("TestButton")

assert definition is not None
assert definition.props["class_name"].html_name == "class"
assert definition.props["disabled"].kind == "boolean"
assert definition.props["label"].kind == "text"

print("Registry HTML metadata: PASS")

# Verify the metadata shape expected by the update protocol.
component = Component(
    type="TestButton",
    props={
        "class_name": State("active"),
        "disabled": State(False),
        "label": State("Save"),
    },
)

class_prop = definition.props["class_name"]
disabled_prop = definition.props["disabled"]
label_prop = definition.props["label"]

assert class_prop.html_name == "class"
assert disabled_prop.html_name == "disabled"
assert label_prop.html_name is None

print("DOM mapping metadata: PASS")

print()
print("=== REGISTRY DOM METADATA TEST PASS ===")
