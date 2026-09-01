import threading
import time
from urllib.request import urlopen

import pylage as ps
from pylage.runtime import Runtime


print("=== PYLAGE SERVE MODE TEST ===")

app = ps.Column(
    ps.Heading("Served App"),
    ps.Button("Hello"),
)

runtime = Runtime(
    app,
    title="Served App",
    output="test_output/serve_output/index.html",
)

try:
    output = runtime.render()
    url = runtime.start()

    print("Output:", output)
    print("URL:", url)

    with urlopen(url) as response:
        body = response.read().decode("utf-8")

        print("Status:", response.status)
        print("Title:", "<title>Served App</title>" in body)
        print("Heading:", "Served App" in body)
        print("Button:", "Hello" in body)

        assert response.status == 200
        assert "<title>Served App</title>" in body
        assert "Served App" in body
        assert "Hello" in body

finally:
    runtime.stop()

print("Runtime stopped.")
print("=== SERVE MODE PASS ===")
