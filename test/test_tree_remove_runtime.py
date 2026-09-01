import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_remove_is_broadcast_when_component_is_removed():
    root = Component(type="Column")

    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    root.add(child)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.remove(child)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_remove"
    assert message["parent_id"] == root.id
    assert message["component_ids"] == [child.id]

    loop.close()

def test_tree_remove_broadcast_contains_removed_subtree_root_id():
    root = Component(type="Column")

    parent = Component(type="Column")
    child = Component(type="Button")

    parent.add(child)
    root.add(parent)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.remove(parent)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_remove"
    assert message["parent_id"] == root.id
    assert message["component_ids"] == [parent.id]

    # Removing the subtree root is enough.
    # The browser DOM removes its complete subtree automatically.
    assert child.id not in message["component_ids"]

    loop.close()
