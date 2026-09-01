import copy
import json

import pytest

from pylage.core.component import Component
from pylage.core.snapshot import component_to_snapshot
from pylage.core.state import State


def test_component_to_snapshot_serializes_component():
    button = Component(
        type="Button",
        props={"text": "Hello"},
    )

    snapshot = component_to_snapshot(button)

    assert snapshot == {
        "id": button.id,
        "type": "Button",
        "tag": "button",
        "events": "",
        "props": {
            "text": "Hello",
        },
        "children": [],
    }


def test_component_to_snapshot_serializes_nested_children():
    root = Component(type="Column")

    child = Component(
        type="Button",
        props={"text": "Child"},
    )

    nested = Component(
        type="Text",
        props={"text": "Nested"},
    )

    child.add(nested)
    root.add(child)

    snapshot = component_to_snapshot(root)

    assert snapshot["id"] == root.id
    assert snapshot["type"] == "Column"
    assert snapshot["tag"] == "div"

    assert len(snapshot["children"]) == 1

    child_snapshot = snapshot["children"][0]

    assert child_snapshot["id"] == child.id
    assert child_snapshot["type"] == "Button"
    assert child_snapshot["tag"] == "button"

    assert len(child_snapshot["children"]) == 1

    nested_snapshot = child_snapshot["children"][0]

    assert nested_snapshot["id"] == nested.id
    assert nested_snapshot["type"] == "Text"
    assert nested_snapshot["tag"] == "div"


def test_component_to_snapshot_serializes_event_names():
    button = Component(type="Button")

    button.on("click", lambda: None)
    button.on("focus", lambda: None)

    snapshot = component_to_snapshot(button)

    assert snapshot["events"] == "click,focus"


def test_component_to_snapshot_ignores_non_component_children():
    root = Component(type="Column")

    root.add(
        "plain text",
        123,
        Component(type="Button"),
    )

    snapshot = component_to_snapshot(root)

    assert len(snapshot["children"]) == 1
    assert snapshot["children"][0]["type"] == "Button"


def test_component_to_snapshot_unknown_component_uses_div_tag():
    component = Component(
        type="UnknownComponent",
        props={"foo": "bar"},
    )

    snapshot = component_to_snapshot(component)

    assert snapshot["type"] == "UnknownComponent"
    assert snapshot["tag"] == "div"
    assert snapshot["props"] == {"foo": "bar"}


def test_snapshot_state_prop_uses_current_state_value():
    state = State("initial")

    component = Component(
        type="Button",
        props={"text": state},
    )

    snapshot = component_to_snapshot(component)

    assert snapshot["props"]["text"] == "initial"
    assert not isinstance(snapshot["props"]["text"], State)

    state.set("updated")

    assert snapshot["props"]["text"] == "initial"


def test_snapshot_nested_state_is_unwrapped_recursively():
    state = State(
        {
            "user": {
                "name": "Racit",
                "roles": ["admin", "developer"],
            },
            "count": 3,
        }
    )

    component = Component(
        type="Column",
        props={"data": state},
    )

    snapshot = component_to_snapshot(component)

    assert snapshot["props"]["data"] == {
        "user": {
            "name": "Racit",
            "roles": ["admin", "developer"],
        },
        "count": 3,
    }


def test_snapshot_preserves_event_registration_order():
    button = Component(type="Button")

    button.on("click", lambda: None)
    button.on("focus", lambda: None)
    button.on("submit", lambda: None)

    snapshot = component_to_snapshot(button)

    assert snapshot["events"] == "click,focus,submit"


def test_snapshot_unknown_component_is_still_serializable():
    component = Component(
        type="FutureComponent",
        props={
            "value": State(
                {
                    "enabled": True,
                    "items": [1, 2, 3],
                }
            )
        },
    )

    snapshot = component_to_snapshot(component)

    assert snapshot["type"] == "FutureComponent"
    assert snapshot["tag"] == "div"
    assert json.dumps(snapshot)


def test_snapshot_is_json_serializable():
    component = Component(
        type="Button",
        props={
            "text": State("Save"),
            "disabled": State(False),
            "metadata": {
                "count": 5,
                "items": ["a", "b"],
            },
        },
    )

    snapshot = component_to_snapshot(component)

    encoded = json.dumps(snapshot)
    decoded = json.loads(encoded)

    assert decoded == snapshot


def test_snapshot_immutability_for_nested_props():
    metadata = {
        "user": {
            "name": "Racit",
        },
        "items": ["one", "two"],
    }

    component = Component(
        type="Button",
        props={"metadata": metadata},
    )

    snapshot = component_to_snapshot(component)

    metadata["user"]["name"] = "Changed"
    metadata["items"].append("three")

    assert snapshot["props"]["metadata"] == {
        "user": {
            "name": "Racit",
        },
        "items": ["one", "two"],
    }


def test_snapshot_immutability_against_component_prop_replacement():
    component = Component(
        type="Button",
        props={
            "text": "Before",
        },
    )

    snapshot = component_to_snapshot(component)

    component.props["text"] = "After"

    assert snapshot["props"]["text"] == "Before"


def test_snapshot_immutability_with_nested_state_value():
    value = {
        "user": {
            "name": "Racit",
        }
    }

    state = State(value)

    component = Component(
        type="Button",
        props={"data": state},
    )

    snapshot = component_to_snapshot(component)

    value["user"]["name"] = "Changed"

    assert snapshot["props"]["data"]["user"]["name"] == "Racit"

    state.set(
        {
            "user": {
                "name": "Updated",
            }
        }
    )

    assert snapshot["props"]["data"]["user"]["name"] == "Racit"


def test_snapshot_does_not_share_mutable_children():
    child = Component(
        type="Button",
        props={
            "data": {
                "items": ["original"],
            }
        },
    )

    root = Component(type="Column")
    root.add(child)

    snapshot = component_to_snapshot(root)

    child.props["data"]["items"].append("changed")

    assert snapshot["children"][0]["props"]["data"] == {
        "items": ["original"],
    }


def test_snapshot_rejects_non_json_serializable_prop():
    component = Component(
        type="Button",
        props={
            "callback": lambda: None,
        },
    )

    with pytest.raises(TypeError, match="JSON serializable"):
        component_to_snapshot(component)
