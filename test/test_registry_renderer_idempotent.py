from pylage.core.registry import registry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY RENDERER IDEMPOTENCY TEST ===")


# First renderer initialization.
renderer1 = HTMLRenderer()

callbacks1 = {
    name: registry.require(name).renderer
    for name in (
        "Column",
        "Heading",
        "Button",
        "Input",
    )
}

for name, callback in callbacks1.items():
    assert callback is not None, (
        f"Missing renderer after first initialization: {name}"
    )

print("First renderer registration: PASS")


# Second renderer initialization must not destroy
# or replace already registered callbacks.
renderer2 = HTMLRenderer()

callbacks2 = {
    name: registry.require(name).renderer
    for name in (
        "Column",
        "Heading",
        "Button",
        "Input",
    )
}

for name in callbacks1:
    assert callbacks2[name] is callbacks1[name], (
        f"Renderer callback changed for {name}"
    )

print("Repeated initialization preserves callbacks: PASS")


# Both renderer instances must still work.
from pylage.components import Heading, Button

heading_html = renderer1.render(
    Heading("Hello")
)

button_html = renderer2.render(
    Button("Save")
)

assert "<h1" in heading_html
assert "Hello" in heading_html

assert "<button" in button_html
assert "Save" in button_html

print("Renderer functionality after repeated initialization: PASS")


print()
print("=== REGISTRY RENDERER IDEMPOTENCY PASS ===")
