from pylage.core.component import Component
from pylage.core.registry import PropDefinition, registry
from pylage.core.renderer import render


print("=== PYLAGE GENERIC VOID RENDER TEST ===")

registry.register(
    "Divider",
    "hr",
    void=True,
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

divider = Component(
    type="Divider",
    props={
        "class_name": "separator",
        "title": "Section divider",
    },
)

html = render(divider)

print(html)

assert "<hr " in html
assert 'class="separator"' in html
assert 'title="Section divider"' in html
assert "</hr>" not in html

definition = registry.require("Divider")

assert definition.void is True
assert definition.tag == "hr"

print("Registry void contract: PASS")
print("Generic void rendering: PASS")
print("Void has no closing tag: PASS")
print()
print("=== GENERIC VOID RENDER PASS ===")
