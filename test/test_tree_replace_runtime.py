import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_replace_is_broadcast_when_component_is_replaced():
    root = Component(type="Column")

    old_child = Component(
        type="Button",
        props={"text": "Old"},
    )

    new_child = Component(
        type="Text",
        props={"text": "New"},
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

    root.replace(old_child, new_child)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_replace"
    assert message["parent_id"] == root.id
    assert message["old_component_id"] == old_child.id
    assert message["index"] == 0

    component = message["new_component"]

    assert component["id"] == new_child.id
    assert component["type"] == "Text"
    assert component["props"]["text"] == "New"

    loop.close()


def test_tree_replace_broadcast_contains_nested_children():
    root = Component(type="Column")

    old_child = Component(
        type="Button",
        props={"text": "Old"},
    )

    new_child = Component(type="Column")

    nested = Component(
        type="Button",
        props={"text": "Nested"},
    )

    new_child.add(nested)
    root.add(old_child)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.replace(old_child, new_child)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_replace"
    assert message["old_component_id"] == old_child.id

    replacement = message["new_component"]

    assert replacement["id"] == new_child.id
    assert replacement["type"] == "Column"
    assert replacement["children"]

    child = replacement["children"][0]

    assert child["id"] == nested.id
    assert child["type"] == "Button"
    assert child["props"]["text"] == "Nested"

    loop.close()


def test_tree_replace_broadcast_serializes_deep_nested_tree():
    root = Component(type="Column")

    old_child = Component(type="Button")

    replacement = Component(type="Column")
    level_one = Component(type="Column")
    level_two = Component(type="Column")
    leaf = Component(
        type="Button",
        props={"text": "Deep"},
    )

    level_two.add(leaf)
    level_one.add(level_two)
    replacement.add(level_one)
    root.add(old_child)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    root.replace(old_child, replacement)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    tree = message["new_component"]

    assert tree["id"] == replacement.id
    assert tree["children"][0]["id"] == level_one.id
    assert tree["children"][0]["children"][0]["id"] == level_two.id
    assert (
        tree["children"][0]["children"][0]["children"][0]["id"]
        == leaf.id
    )
    assert (
        tree["children"][0]["children"][0]["children"][0]["props"]["text"]
        == "Deep"
    )

    loop.close()
