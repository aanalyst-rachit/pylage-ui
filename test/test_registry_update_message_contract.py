import json

from pylage.core.protocol import UpdateMessage


print("=== PYLAGE REGISTRY UPDATE MESSAGE CONTRACT TEST ===")


# ------------------------------------------------------------
# 1. UpdateMessage must support registry metadata.
# ------------------------------------------------------------

message = UpdateMessage(
    component_id="component-1",
    props={
        "class_name": "active",
        "disabled": True,
        "label": "Save",
    },
    prop_meta={
        "class_name": {
            "kind": "attribute",
            "html_name": "class",
        },
        "disabled": {
            "kind": "boolean",
            "html_name": "disabled",
        },
        "label": {
            "kind": "text",
            "html_name": None,
        },
    },
)

payload = message.to_dict()

assert payload["type"] == "update"
assert payload["id"] == "component-1"
assert payload["props"]["class_name"] == "active"

assert payload["prop_meta"]["class_name"]["kind"] == "attribute"
assert payload["prop_meta"]["class_name"]["html_name"] == "class"

assert payload["prop_meta"]["disabled"]["kind"] == "boolean"
assert payload["prop_meta"]["disabled"]["html_name"] == "disabled"

assert payload["prop_meta"]["label"]["kind"] == "text"

print("Registry metadata serialization: PASS")


# ------------------------------------------------------------
# 2. JSON round-trip must preserve metadata.
# ------------------------------------------------------------

raw = message.to_json()

decoded = UpdateMessage.from_json(raw)

assert decoded.component_id == "component-1"
assert decoded.props == {
    "class_name": "active",
    "disabled": True,
    "label": "Save",
}

assert decoded.prop_meta == {
    "class_name": {
        "kind": "attribute",
        "html_name": "class",
    },
    "disabled": {
        "kind": "boolean",
        "html_name": "disabled",
    },
    "label": {
        "kind": "text",
        "html_name": None,
    },
}

print("Registry metadata JSON round-trip: PASS")


# ------------------------------------------------------------
# 3. Existing UpdateMessage shape remains usable.
# ------------------------------------------------------------

legacy = UpdateMessage(
    component_id="component-2",
    props={"title": "Hello"},
)

assert legacy.to_dict()["props"]["title"] == "Hello"

print("Backward-compatible UpdateMessage: PASS")


print()
print("=== REGISTRY UPDATE MESSAGE CONTRACT PASS ===")
