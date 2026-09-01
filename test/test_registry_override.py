from pylage.core.component import Component
from pylage.core.registry import ComponentRegistry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY OVERRIDE TEST ===")


def render_custom(renderer, component):
    return '<article data-custom="yes">CUSTOM</article>'


# Use an isolated registry so this test cannot pollute
# the global builtin registry.
registry = ComponentRegistry()

registry.register(
    "Heading",
    "h1",
    props={
        "text": __import__(
            "pylage.core.registry",
            fromlist=["PropDefinition"],
        ).PropDefinition(
            "text",
            kind="text",
        ),
    },
)

renderer = HTMLRenderer()

# HTMLRenderer.registry is read-only, but its backing registry
# can be selected through construction only if supported.
# For this test, directly exercise the isolated registry contract.
registry.register(
    "Heading",
    "article",
    renderer=render_custom,
)

heading = Component(
    type="Heading",
    props={"text": "Hello"},
)

definition = registry.require("Heading")

assert definition.tag == "article"
assert definition.renderer is render_custom

result = definition.renderer(renderer, heading)

print(result)

assert result == '<article data-custom="yes">CUSTOM</article>'

print("Custom override preserved: PASS")
print()
print("=== REGISTRY OVERRIDE PASS ===")
