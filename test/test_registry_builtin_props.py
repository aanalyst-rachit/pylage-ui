import pylage as ps
from pylage.core.component import Component
from pylage.core.renderer import render


print("=== PYLAGE BUILTIN PROP CONTRACT TEST ===")


# ---------------------------------------------------------
# Heading
# ---------------------------------------------------------
heading = Component(
    type="Heading",
    props={
        "text": "Hello",
    },
)

html = render(heading)

print(html)

assert "<h1" in html
assert "Hello" in html
assert 'data-pylage-id="' in html

print("Heading text contract: PASS")


# ---------------------------------------------------------
# Button attributes
# ---------------------------------------------------------
button = Component(
    type="Button",
    props={
        "text": "Save",
        "value": "save",
        "disabled": True,
        "title": "Save button",
    },
)

html = render(button)

print(html)

assert "<button" in html
assert "Save" in html
assert 'value="save"' in html
assert "disabled" in html
assert 'title="Save button"' in html

print("Button prop contract: PASS")


# ---------------------------------------------------------
# Button boolean false
# ---------------------------------------------------------
button = Component(
    type="Button",
    props={
        "text": "Save",
        "disabled": False,
    },
)

html = render(button)

print(html)

assert "disabled" not in html

print("Boolean false contract: PASS")


# ---------------------------------------------------------
# Input attributes
# ---------------------------------------------------------
input_component = Component(
    type="Input",
    props={
        "value": "Dollar",
        "disabled": True,
        "title": "Name input",
    },
)

html = render(input_component)

print(html)

assert "<input" in html
assert 'value="Dollar"' in html
assert "disabled" in html
assert 'title="Name input"' in html
assert "</input>" not in html

print("Input prop contract: PASS")


print()
print("=== BUILTIN PROP CONTRACT PASS ===")
