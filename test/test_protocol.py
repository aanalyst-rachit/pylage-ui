from pylage.core.protocol import EventMessage


print("=== PYLAGE EVENT PROTOCOL TEST ===")


message = EventMessage(
    component_id="abc123",
    event="click",
)

print("Dict:", message.to_dict())
print("JSON:", message.to_json())

assert message.type == "event"
assert message.to_dict() == {
    "type": "event",
    "id": "abc123",
    "event": "click",
}

decoded = EventMessage.from_json(message.to_json())

assert decoded == message

print("Round trip:", decoded)


payload_message = EventMessage(
    component_id="xyz789",
    event="change",
    payload={"value": "hello"},
)

encoded = payload_message.to_json()

print("Payload JSON:", encoded)

decoded_payload = EventMessage.from_json(encoded)

assert decoded_payload.component_id == "xyz789"
assert decoded_payload.event == "change"
assert decoded_payload.payload == {"value": "hello"}

print("Payload round trip:", decoded_payload)

print("=== EVENT PROTOCOL PASS ===")
