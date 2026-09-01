import pylage as ps


app = ps.Column(
    ps.Heading("Hello PyLage"),
    ps.Button("Click me", variant="primary"),
)

output = ps.run(
    app,
    title="My PyLage App",
    output="test_output/index.html",
)

print("=== PYLAGE RUN TEST ===")
print("Output:", output)
print("Exists:", output.exists())
print("Size:", output.stat().st_size, "bytes")
