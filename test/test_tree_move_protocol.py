from pylage.core.protocol import TreeMoveMessage


def test_tree_move_message_round_trip():
    message = TreeMoveMessage(
        component_id="child123",
        old_parent_id="parentA",
        new_parent_id="parentB",
    )

    assert message.type == "tree_move"

    encoded = message.to_json()
    decoded = TreeMoveMessage.from_json(encoded)

    assert decoded == message


def test_tree_move_message_dict_contract():
    message = TreeMoveMessage(
        component_id="child123",
        old_parent_id="parentA",
        new_parent_id="parentB",
    )

    assert message.to_dict() == {
        "type": "tree_move",
        "component_id": "child123",
        "old_parent_id": "parentA",
        "new_parent_id": "parentB",
    }


def test_tree_move_message_requires_component_id():
    try:
        TreeMoveMessage(
            component_id="",
            old_parent_id="parentA",
            new_parent_id="parentB",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty component_id must raise ValueError"
        )


def test_tree_move_message_requires_parent_ids():
    try:
        TreeMoveMessage(
            component_id="child123",
            old_parent_id="",
            new_parent_id="parentB",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty old_parent_id must raise ValueError"
        )

    try:
        TreeMoveMessage(
            component_id="child123",
            old_parent_id="parentA",
            new_parent_id="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty new_parent_id must raise ValueError"
        )
