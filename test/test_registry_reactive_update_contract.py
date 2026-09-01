from pylage.core.component import Component
from pylage.core.registry import ComponentRegistry, PropDefinition
from pylage.core.state import State


print("=== PYLAGE REGISTRY REACTIVE UPDATE CONTRACT TEST ===")


registry = ComponentRegistry()

registry.register(
    "CustomControl",
    "div",
    props={
        "class_name": PropDefinition(
            name="class_name",
            kind="attribute",
            reactive=True,
            html_name="class",
        ),
        "disabled": PropDefinition(
            name="disabled",
            kind="boolean",
            reactive=True,
            html_name="disabled",
        ),
        "label": PropDefinition(
            name="label",
            kind="text",
            reactive=True,
        ),
    },
)


# ------------------------------------------------------------
# 1. Registry metadata must be available.
# ------------------------------------------------------------

definition = registry.require("CustomControl")

assert definition.props is not None

class_prop = definition.props["class_name"]
disabled_prop = definition.props["disabled"]
label_prop = definition.props["label"]

assert class_prop.html_name == "class"
assert class_prop.kind == "attribute"
assert class_prop.reactive is True

assert disabled_prop.html_name == "disabled"
assert disabled_prop.kind == "boolean"
assert disabled_prop.reactive is True

assert label_prop.kind == "text"
assert label_prop.reactive is True

print("Registry reactive metadata: PASS")


# ------------------------------------------------------------
# 2. State must actually emit changes.
# ------------------------------------------------------------

state = State("initial")
changes = []

unsubscribe = state.subscribe(
    lambda old, new: changes.append((old, new))
)

state.set("updated")

assert changes == [("initial", "updated")]

unsubscribe()

print("State change notification: PASS")


# ------------------------------------------------------------
# 3. Component must retain State-backed props.
# ------------------------------------------------------------

component = Component(
    type="CustomControl",
    props={
        "class_name": state,
    },
)

assert component.props["class_name"] is state

print("State-backed component prop: PASS")


print()
print("=== REGISTRY REACTIVE UPDATE CONTRACT PASS ===")
