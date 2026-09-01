from pathlib import Path

import pylage as ps


print("=== PYLAGE RUN COMPATIBILITY TEST ===")

app = ps.Column(
    ps.Heading("Compatibility Test"),
    ps.Button("Click me"),
)

output = ps.run(
    app,
    title="Compatibility Test",
    output="test_output/compat_output/index.html",
)

print("Return type:", type(output).__name__)
print("Output:", output)
print("Exists:", output.exists())

html = Path(output).read_text(encoding="utf-8")

print("Title:", "<title>Compatibility Test</title>" in html)
print("Heading:", "Compatibility Test" in html)
print("Button:", "Click me" in html)

assert isinstance(output, Path)
assert output.exists()
assert "<title>Compatibility Test</title>" in html
assert "Compatibility Test" in html
assert "Click me" in html

print("=== RUN COMPATIBILITY PASS ===")
