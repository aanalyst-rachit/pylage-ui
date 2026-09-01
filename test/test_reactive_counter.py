import asyncio
import json

import pylage as ps
from websockets.asyncio.client import connect
from pylage.runtime.websocket import WebSocketServer


print("=== PYLAGE REACTIVE COUNTER TEST ===")

count = ps.State(0)


def increment():
    count.set(count.value + 1)
    return count.value


button = ps.Button(
    "Increment",
    on_click=increment,
)

heading = ps.Heading(count)

app = ps.Column(
    heading,
    button,
)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Initial:", count.value)
print("Heading ID:", heading.id)
print("Button ID:", button.id)


async def _test_counter():
    async with connect(url) as ws:
        print("WebSocket connected: PASS")

        # Browser simulates clicking Increment.
        await ws.send(
            json.dumps({
                "type": "event",
                "id": button.id,
                "event": "click",
            })
        )

        # Python callback should update State,
        # and StateBinding should broadcast an update.
        while True:
            raw = await asyncio.wait_for(
                ws.recv(),
                timeout=2,
            )

            print("Received:", raw)

            message = json.loads(raw)

            if message["type"] == "update":
                break

        assert message["type"] == "update"
        assert message["id"] == heading.id
        assert message["props"]["text"] == 1

        print("Event → Python callback: PASS")
        print("Python callback → State.set(): PASS")
        print("State → UpdateMessage: PASS")
        print("Update component ID: PASS")
        print("Updated value: PASS")

        # Second click.
        await ws.send(
            json.dumps({
                "type": "event",
                "id": button.id,
                "event": "click",
            })
        )

        while True:
            raw = await asyncio.wait_for(
                ws.recv(),
                timeout=2,
            )

            print("Received:", raw)

            message = json.loads(raw)

            if message["type"] == "update":
                break

        assert message["type"] == "update"
        assert message["id"] == heading.id
        assert message["props"]["text"] == 2

        print("Second click/state update: PASS")


def test_sync_wrapper():
    try:
        asyncio.run(_test_counter())
    finally:
        server.stop()

    print("Final state:", count.value)
    print("=== PYLAGE REACTIVE COUNTER PASS ===")
