import asyncio
import json

from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer


def test_tree_add_is_broadcast_when_component_is_added():
    root = Component(type="Column")

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    root.add(child)

    loop.run_until_complete(asyncio.sleep(0))

    message = json.loads(messages[0])

    assert message["type"] == "tree_add"
    assert message["parent_id"] == root.id
    assert message["components"][0]["id"] == child.id
    assert message["components"][0]["type"] == "Button"

    loop.close()

def test_tree_add_contains_render_metadata_for_button():
    root = Component(type="Column")

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    root.add(child)

    loop.run_until_complete(asyncio.sleep(0))

    message = json.loads(messages[0])
    component = message["components"][0]

    assert component["type"] == "Button"
    assert component["tag"] == "button"

    loop.close()

def test_tree_add_contains_event_metadata():
    root = Component(type="Column")

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    child.on("click", lambda: "clicked")

    root.add(child)

    loop.run_until_complete(asyncio.sleep(0))

    message = json.loads(messages[0])
    component = message["components"][0]

    assert component["events"] == "click"

    loop.close()


def test_tree_add_contains_insert_index():
    root = Component(type="Column")

    first = Component(
        type="Button",
        props={"text": "First"},
    )

    root.add(first)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    second = Component(
        type="Button",
        props={"text": "Second"},
    )

    root.insert(0, second)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_add"
    assert message["parent_id"] == root.id
    assert message["index"] == 0
    assert message["components"][0]["id"] == second.id

    loop.close()


def test_tree_add_preserves_insert_index_in_message():
    root = Component(type="Column")

    first = Component(
        type="Button",
        props={"text": "First"},
    )

    root.add(first)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    second = Component(
        type="Button",
        props={"text": "Second"},
    )

    root.insert(0, second)

    loop.run_until_complete(asyncio.sleep(0))

    message = json.loads(messages[0])

    assert message["index"] == 0
    assert message["components"][0]["props"]["text"] == "Second"

    loop.close()


def test_tree_add_multiple_components_preserves_index():
    root = Component(type="Column")

    first = Component(
        type="Button",
        props={"text": "First"},
    )

    root.add(first)

    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    second = Component(
        type="Button",
        props={"text": "Second"},
    )

    third = Component(
        type="Button",
        props={"text": "Third"},
    )

    root.insert(1, second, third)

    loop.run_until_complete(asyncio.sleep(0))

    assert len(messages) == 1

    message = json.loads(messages[0])

    assert message["type"] == "tree_add"
    assert message["parent_id"] == root.id
    assert message["index"] == 1

    components = message["components"]

    assert len(components) == 2
    assert components[0]["id"] == second.id
    assert components[1]["id"] == third.id

    assert components[0]["props"]["text"] == "Second"
    assert components[1]["props"]["text"] == "Third"

    loop.close()
