from pylage.core.component import component
from pylage.core.registry import PropDefinition, registry


print("=== PYLAGE COMPONENT REGISTRY CONTRACT TEST ===")


# ---------------------------------------------------------
# Built-in component contract
# ---------------------------------------------------------
button = component(
    "Button",
    text="Save",
    value="save",
    disabled=True,
    title="Save button",
)

print(button)

assert button.type == "Button"
assert button.props["text"] == "Save"
assert button.props["value"] == "save"
assert button.props["disabled"] is True
assert button.props["title"] == "Save button"

print("Built-in props accepted: PASS")


# ---------------------------------------------------------
# Event props remain events
# ---------------------------------------------------------
called = []


def clicked():
    called.append(True)


button = component(
    "Button",
    text="Click",
    on_click=clicked,
)

assert "click" in button.events
assert button.events["click"] is clicked
assert "on_click" not in button.props

print("Event props separated: PASS")


# ---------------------------------------------------------
# Custom registered component
# ---------------------------------------------------------
registry.register(
    "Card",
    "section",
    props={
        "title": PropDefinition(
            "title",
            kind="text",
        ),
        "hidden": PropDefinition(
            "hidden",
            kind="boolean",
        ),
    },
)

card = component(
    "Card",
    title="Hello",
    hidden=True,
)

assert card.type == "Card"
assert card.props["title"] == "Hello"
assert card.props["hidden"] is True

print("Custom registered props accepted: PASS")


# ---------------------------------------------------------
# Unknown component remains backward compatible
# ---------------------------------------------------------
custom = component(
    "UnknownWidget",
    foo="bar",
    answer=42,
)

assert custom.props["foo"] == "bar"
assert custom.props["answer"] == 42

print("Unknown component compatibility: PASS")


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
print("=== COMPONENT REGISTRY CONTRACT PASS ===")
