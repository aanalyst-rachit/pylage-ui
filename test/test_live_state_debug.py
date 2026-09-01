import time

import pylage as ps
from pylage.runtime import Runtime


print("=== PYLAGE LIVE STATE DEBUG ===")

count = ps.State(0)

app = ps.Column(
    ps.Heading(count),
)

runtime = Runtime(
    app,
    title="PyLage Live State Debug",
    output="test_output/live_state_debug/index.html",
)

try:
    url = runtime.start()

    print("HTTP:", url)
    print("WebSocket:", runtime._websocket.url)
    print("Component:", app.children[0].id)
    print("Initial:", count.value)
    print()
    print("OPEN THIS URL:")
    print(url)
    print()
    print("Keep browser open.")
    print("State updates will be sent every 2 seconds.")
    print("Expected browser values: 1, 2, 3, 4, 5...")
    print()
    
    value = 0

    while True:
        time.sleep(2)

        value += 1
        print(f">>> Python State.set({value})")

        count.set(value)

        print(">>> State now:", count.value)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    runtime.stop()
    print("Runtime stopped.")
