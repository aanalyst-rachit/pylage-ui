import inspect

from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY RENDERER OWNERSHIP TEST ===")


source = inspect.getsource(HTMLRenderer._register_builtin_renderers)


# The registration mechanism itself should be generic.
assert "self.registry.get(component_type)" in source
assert "self.registry.set_renderer(" in source

print("Renderer attachment uses registry API: PASS")


# Builtin names may be declared as registration data,
# but _render_component must remain completely generic.
component_source = inspect.getsource(
    HTMLRenderer._render_component
)

for name in (
    "Column",
    "Heading",
    "Button",
    "Input",
):
    assert f'"{name}"' not in component_source
    assert f"'{name}'" not in component_source

print("Component dispatch remains generic: PASS")


# Renderer must actually invoke the registry-owned callback.
assert "definition.renderer" in component_source
assert "definition.renderer(self, component)" in component_source

print("Registry-owned renderer invocation: PASS")


print()
print("=== REGISTRY RENDERER OWNERSHIP PASS ===")
