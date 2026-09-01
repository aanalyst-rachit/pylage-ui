from pylage.core.protocol import TreeRemoveMessage


def test_tree_remove_message_round_trip():
    message = TreeRemoveMessage(
        parent_id="parent123",
        component_ids=["child456"],
    )

    assert message.type == "tree_remove"

    encoded = message.to_json()
    decoded = TreeRemoveMessage.from_json(encoded)

    assert decoded == message


def test_tree_remove_message_dict_contract():
    message = TreeRemoveMessage(
        parent_id="root123",
        component_ids=["button123", "input456"],
    )

    assert message.to_dict() == {
        "type": "tree_remove",
        "parent_id": "root123",
        "component_ids": [
            "button123",
            "input456",
        ],
    }


def test_tree_remove_message_requires_parent_id():
    try:
        TreeRemoveMessage(
            parent_id="",
            component_ids=[],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )
