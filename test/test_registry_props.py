from pylage.core.registry import (
    ComponentRegistry,
    PropDefinition,
)


print("=== PYLAGE REGISTRY PROPS TEST ===")

registry = ComponentRegistry()

definition = registry.register(
    "Button",
    "button",
    props={
        "text": PropDefinition(
            "text",
            kind="text",
        ),
        "disabled": PropDefinition(
            "disabled",
            kind="boolean",
        ),
    },
)

assert definition.props is not None
assert "text" in definition.props
assert "disabled" in definition.props

assert definition.props["text"].name == "text"
assert definition.props["text"].kind == "text"

assert definition.props["disabled"].name == "disabled"
assert definition.props["disabled"].kind == "boolean"

print("Prop registration: PASS")
print("Prop metadata storage: PASS")
print("Prop definition contract: PASS")
print()
print("=== REGISTRY PROPS PASS ===")
