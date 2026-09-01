
import threading
import time

import pylage as ps
from pylage.runtime import Runtime


print("=== PYLAGE LIVE BROWSER STATE TEST ===")

count = ps.State(0)

app = ps.Column(
    ps.Heading(count),
)

runtime = Runtime(
    app,
    title="PyLage Live State",
    output="test_output/live_state_output/index.html",
)

try:
    url = runtime.start()

    print()
    print("HTTP:", url)
    print("WebSocket:", runtime._websocket.url)
    print("Component ID:", app.children[0].id)
    print("Initial value:", count.value)

    print()
    print("Open this URL in your browser:")
    print(url)

    print()
    print("Browser should initially show: 0")
    print("After 5 seconds Python will send: 42")
    print()

    def update_state():
        time.sleep(5)
        print(">>> Python: count.set(42)")
        count.set(42)
        print(">>> Update sent.")

    thread = threading.Thread(
        target=update_state,
        daemon=True,
    )
    thread.start()

    print("Server is running.")
    print("Press Ctrl+C after confirming browser changed 0 -> 42.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print()
    print("Stopping...")

finally:
    runtime.stop()
    print("Runtime stopped.")
