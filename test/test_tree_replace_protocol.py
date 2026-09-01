from pylage.core.protocol import TreeReplaceMessage


def test_tree_replace_message_round_trip():
    message = TreeReplaceMessage(
        parent_id="parent123",
        old_component_id="old456",
        new_component={
            "id": "new789",
            "type": "Text",
            "tag": "span",
            "props": {
                "text": "Replaced",
            },
            "children": [],
        },
        index=2,
    )

    assert message.type == "tree_replace"

    encoded = message.to_json()
    decoded = TreeReplaceMessage.from_json(encoded)

    assert decoded == message


def test_tree_replace_message_dict_contract():
    message = TreeReplaceMessage(
        parent_id="parent123",
        old_component_id="old456",
        new_component={
            "id": "new789",
            "type": "Text",
            "tag": "span",
            "props": {
                "text": "Replaced",
            },
            "children": [],
        },
        index=2,
    )

    assert message.to_dict() == {
        "type": "tree_replace",
        "parent_id": "parent123",
        "old_component_id": "old456",
        "new_component": {
            "id": "new789",
            "type": "Text",
            "tag": "span",
            "props": {
                "text": "Replaced",
            },
            "children": [],
        },
        "index": 2,
    }


def test_tree_replace_message_requires_parent_id():
    try:
        TreeReplaceMessage(
            parent_id="",
            old_component_id="old456",
            new_component={
                "id": "new789",
                "type": "Text",
            },
            index=0,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )
