import pylage as ps
from pylage.core.events import EventDispatcher


print("=== PYLAGE EVENT DISPATCH TEST ===")

calls = []


def clicked():
    calls.append("clicked")


def changed(value):
    calls.append(value)


button = ps.Button(
    "Click me",
    on_click=clicked,
    on_change=changed,
)

app = ps.Column(button)

dispatcher = EventDispatcher(app)

print("Component indexed:", dispatcher.has_component(button.id))
print("Click event:", dispatcher.has_event(button.id, "click"))
print("Change event:", dispatcher.has_event(button.id, "change"))

assert dispatcher.has_component(button.id)
assert dispatcher.has_event(button.id, "click")
assert dispatcher.has_event(button.id, "change")

result = dispatcher.dispatch(
    button.id,
    "click",
)

dispatcher.dispatch(
    button.id,
    "change",
    {"value": "hello"},
)

print("Click result:", result)
print("Calls:", calls)

assert calls == [
    "clicked",
    {"value": "hello"},
]

print("=== EVENT DISPATCH PASS ===")
