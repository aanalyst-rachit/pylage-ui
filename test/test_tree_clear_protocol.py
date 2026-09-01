from pylage.core.protocol import TreeClearMessage


def test_tree_clear_message_round_trip():
    message = TreeClearMessage(
        parent_id="parent123",
        component_ids=["child1", "child2", "child3"],
    )

    assert message.type == "tree_clear"

    encoded = message.to_json()
    decoded = TreeClearMessage.from_json(encoded)

    assert decoded == message


def test_tree_clear_message_dict_contract():
    message = TreeClearMessage(
        parent_id="parent123",
        component_ids=["child1", "child2"],
    )

    assert message.to_dict() == {
        "type": "tree_clear",
        "parent_id": "parent123",
        "component_ids": ["child1", "child2"],
    }


def test_tree_clear_message_requires_parent_id():
    try:
        TreeClearMessage(
            parent_id="",
            component_ids=["child1"],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )
