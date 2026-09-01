from pylage.core.protocol import TreeSetChildrenMessage


def test_tree_set_children_message_round_trip():
    message = TreeSetChildrenMessage(
        parent_id="parent123",
        children=[
            {
                "id": "child1",
                "type": "Button",
                "props": {"text": "Hello"},
            },
            {
                "id": "child2",
                "type": "Text",
                "props": {"text": "World"},
            },
        ],
    )

    assert message.type == "tree_set_children"

    encoded = message.to_json()
    decoded = TreeSetChildrenMessage.from_json(encoded)

    assert decoded == message


def test_tree_set_children_message_dict_contract():
    children = [
        {
            "id": "child1",
            "type": "Button",
            "props": {"text": "Hello"},
        }
    ]

    message = TreeSetChildrenMessage(
        parent_id="parent123",
        children=children,
    )

    assert message.to_dict() == {
        "type": "tree_set_children",
        "parent_id": "parent123",
        "children": children,
    }


def test_tree_set_children_message_requires_parent_id():
    try:
        TreeSetChildrenMessage(
            parent_id="",
            children=[],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )
