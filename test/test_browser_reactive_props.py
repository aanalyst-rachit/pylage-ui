import threading
import time
import webbrowser

import pylage as ps
from pylage.core.component import Component
from pylage.runtime import Runtime


print("=== PYLAGE BROWSER GENERIC REACTIVE PROPS TEST ===")

text = ps.State("Hello")
value = ps.State("100")
disabled = ps.State(False)
title = ps.State("Initial title")

button = Component(
    type="Button",
    props={
        "text": text,
        "value": value,
        "disabled": disabled,
        "title": title,
    },
)

app = ps.Column(button)

runtime = Runtime(
    app,
    title="PyLage Generic Reactive Props",
    output="test_output/browser_reactive_props/index.html",
)

url = runtime.start()

print()
print("HTTP:", url)
print("WebSocket:", runtime._websocket.url)
print("Component ID:", button.id)

print()
print("Open this URL:")
print(url)

print()
print("Browser initial state:")
print("  text     = Hello")
print("  value    = 100")
print("  disabled = false")
print("  title    = Initial title")

print()
print("Updates will happen every 3 seconds:")
print("  1. text → World")
print("  2. value → 200")
print("  3. disabled → true")
print("  4. title → Updated title")
print()

try:
    webbrowser.open(url)

    time.sleep(3)

    print(">>> Python: text.set('World')")
    text.set("World")

    time.sleep(3)

    print(">>> Python: value.set('200')")
    value.set("200")

    time.sleep(3)

    print(">>> Python: disabled.set(True)")
    disabled.set(True)

    time.sleep(3)

    print(">>> Python: title.set('Updated title')")
    title.set("Updated title")

    print()
    print("=== ALL UPDATES SENT ===")
    print()
    print("Check the browser DevTools console.")
    print("You should see [PyLage response] update messages.")
    print()
    print("Press Ctrl+C after confirming the DOM changes.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    runtime.stop()
    print("Runtime stopped.")
