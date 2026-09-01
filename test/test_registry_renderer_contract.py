import inspect

from pylage.core.registry import registry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY → RENDERER CONTRACT TEST ===")


# ------------------------------------------------------------
# 1. Every builtin component must exist in registry.
# ------------------------------------------------------------

for component_type in (
    "Column",
    "Heading",
    "Button",
    "Input",
):
    assert registry.has(component_type), (
        f"Missing registry component: {component_type}"
    )

print("Builtin registry coverage: PASS")


# ------------------------------------------------------------
# 2. Every builtin component must have a renderer.
# ------------------------------------------------------------

renderer = HTMLRenderer()

for component_type in (
    "Column",
    "Heading",
    "Button",
    "Input",
):
    definition = registry.require(component_type)

    assert definition.renderer is not None, (
        f"Missing renderer for {component_type}"
    )

    assert callable(definition.renderer), (
        f"Renderer is not callable for {component_type}"
    )

print("Registry renderer attachment: PASS")


# ------------------------------------------------------------
# 3. Renderer must resolve through registry.
# ------------------------------------------------------------

source = inspect.getsource(HTMLRenderer._render_component)

assert "self.registry.get(component_type)" in source

print("Renderer registry resolution: PASS")


# ------------------------------------------------------------
# 4. Registry must expose component contract.
# ------------------------------------------------------------

heading = registry.require("Heading")

assert heading.tag == "h1"
assert heading.props is not None
assert "text" in heading.props

button = registry.require("Button")

assert button.tag == "button"
assert button.props is not None
assert "text" in button.props
assert "value" in button.props
assert "disabled" in button.props
assert "title" in button.props

input_def = registry.require("Input")

assert input_def.tag == "input"
assert input_def.void is True
assert input_def.props is not None
assert "value" in input_def.props
assert "disabled" in input_def.props
assert "title" in input_def.props

print("Component contracts: PASS")


print()
print("=== REGISTRY → RENDERER CONTRACT PASS ===")
