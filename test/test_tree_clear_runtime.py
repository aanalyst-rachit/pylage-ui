import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_clear_is_broadcast_when_children_are_cleared():
    root = Component(type="Column")

    first = Component(
        type="Button",
        props={"text": "First"},
    )

    second = Component(
        type="Text",
        props={"text": "Second"},
    )

    root.add(first, second)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.clear()

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_clear"
    assert message["parent_id"] == root.id
    assert message["component_ids"] == [
        first.id,
        second.id,
    ]

    loop.close()


def test_tree_clear_broadcast_contains_direct_children_only():
    root = Component(type="Column")

    first = Component(type="Column")
    nested = Component(
        type="Button",
        props={"text": "Nested"},
    )

    second = Component(type="Button")

    first.add(nested)
    root.add(first, second)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.clear()

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_clear"
    assert message["parent_id"] == root.id

    assert message["component_ids"] == [
        first.id,
        second.id,
    ]

    assert nested.id not in message["component_ids"]

    loop.close()


def test_tree_clear_does_not_broadcast_when_parent_is_empty():
    root = Component(type="Column")

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.clear()

    loop.run_until_complete(asyncio.sleep(0))

    assert messages == []

    loop.close()
