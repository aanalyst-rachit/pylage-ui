from pylage.core.component import Component
from pylage.core.registry import PropDefinition, registry
from pylage.core.renderer import HTMLRenderer


print("=== PYLAGE REGISTRY GLOBAL PROP ALIAS TEST ===")


# ---------------------------------------------------------
# Register custom component using Python-friendly prop names.
# The HTML names must come entirely from registry metadata.
# ---------------------------------------------------------
registry.register(
    "AliasProbe",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "html_for": PropDefinition(
            "html_for",
            kind="attribute",
            html_name="for",
        ),
    },
)


component = Component(
    type="AliasProbe",
    props={
        "class_name": "probe",
        "html_for": "target",
    },
)


html = HTMLRenderer().render(component)

print(html)

assert 'class="probe"' in html
assert 'for="target"' in html

print("Registry class_name → class: PASS")
print("Registry html_for → for: PASS")


# ---------------------------------------------------------
# Critical architectural contract:
# renderer must NOT contain semantic alias fallback.
# ---------------------------------------------------------
renderer_source = open(
    "pylage/core/renderer.py",
    encoding="utf-8",
).read()

assert '"class_name": "class"' not in renderer_source
assert '"html_for": "for"' not in renderer_source

print("Renderer alias fallback removed: PASS")


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------
registry.unregister("AliasProbe")

print()
print("=== REGISTRY GLOBAL PROP ALIAS PASS ===")
