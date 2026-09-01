from pylage.core.registry import ComponentRegistry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE CUSTOM RENDERER PROTECTION TEST ===")


local_registry = ComponentRegistry()


def custom_renderer(renderer, component):
    return "<custom-rendered></custom-rendered>"


# Register a custom component with its own renderer.
local_registry.register(
    "CustomCard",
    "section",
    renderer=custom_renderer,
)


assert local_registry.require("CustomCard").renderer is custom_renderer

print("Custom renderer registration: PASS")


# Create a renderer and replace its registry with our isolated registry.
renderer = HTMLRenderer(registry_instance=local_registry)


# Built-in registration must not overwrite a renderer
# that is already present.
renderer._register_builtin_renderers()

assert local_registry.require("CustomCard").renderer is custom_renderer

print("Custom renderer preservation: PASS")


# The custom callback must remain callable.
result = local_registry.require("CustomCard").renderer(
    renderer,
    type(
        "DummyComponent",
        (),
        {"type": "CustomCard"},
    )(),
)

assert result == "<custom-rendered></custom-rendered>"

print("Custom renderer remains functional: PASS")


print()
print("=== CUSTOM RENDERER PROTECTION PASS ===")
