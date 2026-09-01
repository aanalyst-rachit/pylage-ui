import inspect

from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY NO BUILTIN DISPATCH TEST ===")

source = inspect.getsource(HTMLRenderer._render_component)

# _render_component itself must not contain explicit builtin
# component-name dispatch.
for component_type in (
    "Column",
    "Heading",
    "Button",
    "Input",
):
    assert f'"{component_type}"' not in source, (
        f"Hard-coded builtin dispatch remains in _render_component: "
        f"{component_type!r}"
    )

    assert f"'{component_type}'" not in source, (
        f"Hard-coded builtin dispatch remains in _render_component: "
        f"{component_type!r}"
    )

print("No builtin dispatch in _render_component: PASS")


# Registry lookup must remain the dispatch mechanism.
assert "self.registry.get(component_type)" in source

print("Registry-driven component resolution: PASS")


print()
print("=== REGISTRY NO BUILTIN DISPATCH TEST PASS ===")
