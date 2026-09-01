import json

print("=== PYLAGE STATE PROTOCOL TEST ===")

message = {
    "type": "update",
    "id": "component123",
    "props": {
        "text": "Hello"
    },
}

encoded = json.dumps(
    message,
    separators=(",", ":"),
)

print("Encoded:", encoded)

decoded = json.loads(encoded)

assert decoded["type"] == "update"
assert decoded["id"] == "component123"
assert decoded["props"]["text"] == "Hello"

print("Type: PASS")
print("Component ID: PASS")
print("Props: PASS")
print("=== STATE PROTOCOL PASS ===")
