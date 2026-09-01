import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_move_is_broadcast_when_component_is_moved():
    root = Component(type="Column")
    old_parent = Component(type="Column")
    new_parent = Component(type="Column")
    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    root.add(old_parent)
    root.add(new_parent)
    old_parent.add(child)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    child.move_to(new_parent)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_move"
    assert message["component_id"] == child.id
    assert message["old_parent_id"] == old_parent.id
    assert message["new_parent_id"] == new_parent.id

    loop.close()
