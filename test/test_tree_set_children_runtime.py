import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_set_children_is_broadcast_when_children_are_replaced():
    root = Component(type="Column")

    old_child = Component(
        type="Button",
        props={"text": "Old"},
    )

    root.add(old_child)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    new_first = Component(
        type="Text",
        props={"text": "First"},
    )

    new_second = Component(
        type="Button",
        props={"text": "Second"},
    )

    root.set_children(new_first, new_second)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_set_children"
    assert message["parent_id"] == root.id

    assert [child["id"] for child in message["children"]] == [
        new_first.id,
        new_second.id,
    ]

    loop.close()


def test_tree_set_children_broadcast_contains_nested_subtree():
    root = Component(type="Column")

    old_child = Component(type="Button")
    root.add(old_child)

    new_parent = Component(type="Column")

    nested = Component(type="Column")

    deep_child = Component(
        type="Button",
        props={"text": "Deep"},
    )

    nested.add(deep_child)
    new_parent.add(nested)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.set_children(new_parent)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_set_children"
    assert message["parent_id"] == root.id

    replacement = message["children"]

    assert len(replacement) == 1
    assert replacement[0]["id"] == new_parent.id
    assert replacement[0]["type"] == "Column"

    nested_payload = replacement[0]["children"]

    assert len(nested_payload) == 1
    assert nested_payload[0]["id"] == nested.id

    deep_payload = nested_payload[0]["children"]

    assert len(deep_payload) == 1
    assert deep_payload[0]["id"] == deep_child.id
    assert deep_payload[0]["props"]["text"] == "Deep"

    loop.close()
