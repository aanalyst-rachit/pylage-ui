from pathlib import Path
from urllib.request import urlopen

from pylage import Button, Column, Heading, run
from pylage.runtime import LocalServer


print("=== PYLAGE RUNTIME LIFECYCLE TEST ===")

app = Column(
    Heading("Runtime Test"),
    Button("Click me"),
)

output = run(
    app,
    title="Runtime Test",
    output="test_output/runtime_output/index.html",
)

print("HTML:", output)
print("HTML exists:", output.exists())

server = LocalServer(output.parent)

try:
    url = server.start()

    print("Server URL:", url)
    print("Server running:", True)

    for request_number in range(1, 4):
        with urlopen(url) as response:
            body = response.read().decode("utf-8")

            print(
                f"Request {request_number}:",
                response.status,
                f"{len(body)} bytes",
            )

            assert response.status == 200
            assert "<title>Runtime Test</title>" in body
            assert "Runtime Test" in body

finally:
    server.stop()

print("Server stopped.")

try:
    urlopen(url)
except Exception as exc:
    print("After stop:", type(exc).__name__)

print("=== RUNTIME LIFECYCLE PASS ===")
