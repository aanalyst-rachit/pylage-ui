import pylage as ps

from pylage.core.renderer import render


print("=== PYLAGE EVENT RENDER TEST ===")


def clicked():
    pass


button = ps.Button(
    "Click me",
    on_click=clicked,
)

html = render(button)

print(html)

assert 'data-pylage-id="' in html
assert 'data-pylage-events="click"' in html
assert ">Click me</button>" in html

# Python callback itself must never appear in HTML.
assert "clicked" not in html

print("Event metadata: PASS")
print("Callback isolation: PASS")


plain_button = ps.Button("Plain")

plain_html = render(plain_button)

assert "data-pylage-events" not in plain_html

print("No-event regression: PASS")

print("=== EVENT RENDER PASS ===")
