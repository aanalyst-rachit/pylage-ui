from pylage.core.protocol import TreeAddMessage


def test_tree_add_message_round_trip():
    message = TreeAddMessage(
        parent_id="parent123",
        components=[
            {
                "id": "child456",
                "type": "Button",
                "props": {
                    "text": "Hello",
                },
                "children": [],
            }
        ],
    )

    assert message.type == "tree_add"

    encoded = message.to_json()
    decoded = TreeAddMessage.from_json(encoded)

    assert decoded == message


def test_tree_add_message_dict_contract():
    message = TreeAddMessage(
        parent_id="root123",
        components=[
            {
                "id": "button123",
                "type": "Button",
                "props": {
                    "text": "Click",
                },
                "children": [],
            }
        ],
    )

    assert message.to_dict() == {
        "type": "tree_add",
        "parent_id": "root123",
        "components": [
            {
                "id": "button123",
                "type": "Button",
                "props": {
                    "text": "Click",
                },
                "children": [],
            }
        ],
    }


def test_tree_add_message_requires_parent_id():
    try:
        TreeAddMessage(
            parent_id="",
            components=[],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )

def test_tree_add_message_preserves_nested_children():
    message = TreeAddMessage(
        parent_id="root123",
        components=[
            {
                "id": "column123",
                "type": "Column",
                "props": {},
                "children": [
                    {
                        "id": "button123",
                        "type": "Button",
                        "props": {
                            "text": "Nested",
                        },
                        "children": [],
                    }
                ],
            }
        ],
    )

    decoded = TreeAddMessage.from_json(message.to_json())

    assert decoded == message
    assert decoded.components[0]["children"][0]["id"] == "button123"



from pylage.core.patch import operation_to_message, operations_to_messages
from pylage.core.protocol import UpdateMessage


def test_replace_operation_converts_to_tree_replace_message():
    operation = {
        "type": "replace",
        "parent_id": "root",
        "id": "child",
        "index": 0,
        "node": {
            "id": "new-child",
            "type": "Button",
            "tag": "div",
            "events": "",
            "props": {"text": "New"},
            "children": [],
        },
    }

    message = operation_to_message(operation)

    assert message.type == "tree_replace"
    assert message.parent_id == "root"
    assert message.old_component_id == "child"
    assert message.index == 0
    assert message.new_component == operation["node"]


def test_replace_operation_requires_parent_id():
    operation = {
        "type": "replace",
        "id": "child",
        "index": 0,
        "node": {
            "id": "new-child",
            "type": "Button",
        },
    }

    try:
        operation_to_message(operation)
    except ValueError as exc:
        assert "valid id" in str(exc)
    else:
        raise AssertionError(
            "Missing parent_id must raise ValueError"
        )


def test_replace_operation_requires_index():
    operation = {
        "type": "replace",
        "parent_id": "root",
        "id": "child",
        "node": {
            "id": "new-child",
            "type": "Button",
        },
    }

    try:
        operation_to_message(operation)
    except ValueError as exc:
        assert "valid index" in str(exc)
    else:
        raise AssertionError(
            "Missing index must raise ValueError"
        )


from pylage.core.patch import operations_to_json


def test_replace_diff_operation_produces_protocol_json():
    operations = [
        {
            "type": "replace",
            "parent_id": "root",
            "id": "child",
            "index": 0,
            "node": {
                "id": "new-child",
                "type": "Button",
                "tag": "div",
                "events": "",
                "props": {"text": "New"},
                "children": [],
            },
        }
    ]

    messages = operations_to_json(operations)

    assert len(messages) == 1

    import json

    message = json.loads(messages[0])

    assert message == {
        "type": "tree_replace",
        "parent_id": "root",
        "old_component_id": "child",
        "new_component": operations[0]["node"],
        "index": 0,
    }


from pylage.core.diff import diff


def test_diff_replace_flows_through_patch_engine():
    previous = {
        "id": "root",
        "type": "Column",
        "tag": "div",
        "events": "",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "tag": "div",
                "events": "",
                "props": {"text": "Old"},
                "children": [],
            }
        ],
    }

    current = {
        "id": "root",
        "type": "Column",
        "tag": "div",
        "events": "",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Button",
                "tag": "div",
                "events": "",
                "props": {"text": "New"},
                "children": [],
            }
        ],
    }

    operations = diff(previous, current)

    assert operations == [
        {
            "type": "replace",
            "parent_id": "root",
            "id": "child",
            "index": 0,
            "node": current["children"][0],
        }
    ]

    messages = operations_to_json(operations)

    import json

    assert json.loads(messages[0]) == {
        "type": "tree_replace",
        "parent_id": "root",
        "old_component_id": "child",
        "new_component": current["children"][0],
        "index": 0,
    }


def test_update_operation_converts_to_protocol_message():
    operation = {
        "type": "update",
        "id": "button",
        "props": {"text": "Save"},
        "remove_props": [],
    }

    message = operation_to_message(operation)

    assert message.type == "update"
    assert message.component_id == "button"
    assert message.props == {"text": "Save"}


def test_update_operation_preserves_remove_props():
    operation = {
        "type": "update",
        "id": "button",
        "props": {},
        "remove_props": ["disabled"],
    }

    message = operation_to_message(operation)

    assert message.type == "update"
    assert message.component_id == "button"
    assert message.props == {}
    assert message.remove_props == ["disabled"]


def test_update_operation_json_preserves_remove_props():
    operation = {
        "type": "update",
        "id": "button",
        "props": {},
        "remove_props": ["disabled"],
    }

    message = operation_to_message(operation)

    import json

    assert json.loads(message.to_json()) == {
        "type": "update",
        "id": "button",
        "props": {},
        "remove_props": ["disabled"],
    }


def test_update_message_round_trip_preserves_remove_props():
    message = UpdateMessage(
        component_id="button",
        props={},
        remove_props=["disabled"],
    )

    decoded = UpdateMessage.from_json(message.to_json())

    assert decoded == message


def test_insert_operation_converts_to_tree_add_message():
    node = {
        "id": "child",
        "type": "Button",
        "tag": "div",
        "events": "",
        "props": {"text": "Add"},
        "children": [],
    }

    operation = {
        "type": "insert",
        "parent_id": "root",
        "index": 1,
        "node": node,
    }

    message = operation_to_message(operation)

    assert message.type == "tree_add"
    assert message.parent_id == "root"
    assert message.components == [node]
    assert message.index == 1


def test_remove_operation_converts_to_tree_remove_message():
    operation = {
        "type": "remove",
        "parent_id": "root",
        "id": "child",
        "index": 1,
    }

    message = operation_to_message(operation)

    assert message.type == "tree_remove"
    assert message.parent_id == "root"
    assert message.component_ids == ["child"]


def test_operations_to_messages_preserves_operation_order():
    operations = [
        {
            "type": "update",
            "id": "first",
            "props": {"text": "A"},
            "remove_props": [],
        },
        {
            "type": "remove",
            "parent_id": "root",
            "id": "second",
            "index": 1,
        },
    ]

    messages = operations_to_messages(operations)

    assert [message.type for message in messages] == [
        "update",
        "tree_remove",
    ]

    assert messages[0].component_id == "first"
    assert messages[1].component_ids == ["second"]
