import pylage as ps

from pylage.core.registry import (
    ComponentRegistry,
    registry,
)


print("=== PYLAGE COMPONENT REGISTRY TEST ===")

assert registry.has("Column")
assert registry.has("Heading")
assert registry.has("Button")
assert registry.has("Input")

assert registry.require("Column").tag == "div"
assert registry.require("Heading").tag == "h1"
assert registry.require("Button").tag == "button"
assert registry.require("Input").tag == "input"
assert registry.require("Input").void is True

custom = ComponentRegistry()

custom.register("Card", "section")

assert custom.has("Card")
assert custom.require("Card").tag == "section"

custom.unregister("Card")

assert not custom.has("Card")

print("Built-in components: PASS")
print("Custom registration: PASS")
print("Unregister: PASS")
print()
print("=== COMPONENT REGISTRY PASS ===")
