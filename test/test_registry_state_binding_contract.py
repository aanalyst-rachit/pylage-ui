from pylage.core.binding import StateBinding
from pylage.core.component import Component
from pylage.core.registry import ComponentRegistry, PropDefinition
from pylage.core.state import State
import pylage.core.binding as binding_module


print("=== PYLAGE REGISTRY STATE BINDING CONTRACT TEST ===")


registry = ComponentRegistry()

registry.register(
    "ReactiveControl",
    "div",
    props={
        "value": PropDefinition(
            name="value",
            kind="attribute",
            reactive=True,
            html_name="data-value",
        ),
        "static_value": PropDefinition(
            name="static_value",
            kind="attribute",
            reactive=False,
            html_name="data-static",
        ),
    },
)


# Use the isolated registry for this contract test without
# mutating the process-wide builtin registry.
original_registry = binding_module.registry
binding_module.registry = registry


reactive_state = State("one")
static_state = State("static-one")

component = Component(
    type="ReactiveControl",
    props={
        "value": reactive_state,
        "static_value": static_state,
    },
)


updates = []

binding = StateBinding(
    component,
    lambda changed_component, props: updates.append(
        (changed_component, props)
    ),
)


# ------------------------------------------------------------
# 1. Reactive prop must be subscribed.
# ------------------------------------------------------------

reactive_state.set("two")

assert updates == [
    (component, {"value": "two"})
]

print("reactive=True binding: PASS")


# ------------------------------------------------------------
# 2. Non-reactive prop must NOT be subscribed.
# ------------------------------------------------------------

static_state.set("static-two")

assert updates == [
    (component, {"value": "two"})
]

print("reactive=False suppression: PASS")


# ------------------------------------------------------------
# 3. Binding must be stoppable.
# ------------------------------------------------------------

binding.stop()

reactive_state.set("three")

assert updates == [
    (component, {"value": "two"})
]

print("Binding unsubscribe: PASS")


print()
print("=== REGISTRY STATE BINDING CONTRACT PASS ===")


# Restore the process-wide builtin registry.
binding_module.registry = original_registry
