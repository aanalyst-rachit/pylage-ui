from urllib.request import urlopen

import pylage as ps
from pylage.runtime import Runtime


print("=== PYLAGE RUNTIME API TEST ===")

app = ps.Column(
    ps.Heading("Hello Runtime"),
    ps.Button("Click me"),
)

runtime = Runtime(
    app,
    title="Runtime API Test",
    output="test_output/runtime_api_output/index.html",
)

print("Before start:", runtime.running)

try:
    url = runtime.start()

    print("Running:", runtime.running)
    print("URL:", url)

    with urlopen(url) as response:
        body = response.read().decode("utf-8")

        print("Status:", response.status)
        print("Title:", "<title>Runtime API Test</title>" in body)
        print("Heading:", "Hello Runtime" in body)

        assert response.status == 200
        assert "<title>Runtime API Test</title>" in body
        assert "Hello Runtime" in body

finally:
    runtime.stop()

print("After stop:", runtime.running)
print("=== RUNTIME API PASS ===")
