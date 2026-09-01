import asyncio
import json

import pylage as ps
from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer

print("=== PYLAGE GENERIC REACTIVE PROPS TEST ===")

text = ps.State("Hello")
value = ps.State("100")
disabled = ps.State(False)
title = ps.State("Initial title")

component = Component(
    type="Button",
    props={
        "text": text,
        "value": value,
        "disabled": disabled,
        "title": title,
    },
)

app = ps.Column(component)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Component ID:", component.id)
print("Initial:")
print("  text =", text.value)
print("  value =", value.value)
print("  disabled =", disabled.value)
print("  title =", title.value)


async def _test_props():
    import websockets

    async with websockets.connect(url) as ws:
        print("WebSocket connected: PASS")

        text.set("World")

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("Received:", message)

        assert message["type"] == "update"
        assert message["id"] == component.id
        assert message["props"]["text"] == "World"

        print("text: PASS")

        value.set("200")

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        assert message["props"]["value"] == "200"

        print("value: PASS")

        disabled.set(True)

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        assert message["props"]["disabled"] is True

        print("disabled: PASS")

        title.set("Updated title")

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        assert message["props"]["title"] == "Updated title"

        print("title: PASS")

        print()
        print("State → UpdateMessage: PASS")
        print("Multiple reactive props: PASS")
        print()
        print("=== GENERIC REACTIVE PROPS PASS ===")


def test_sync_wrapper():
    try:
        asyncio.run(_test_props())
    finally:
        server.stop()
