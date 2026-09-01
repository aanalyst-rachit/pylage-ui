import asyncio
import json

import pylage as ps
from pylage.runtime.websocket import WebSocketServer


print("=== PYLAGE INPUT TWO-WAY BINDING TEST ===")

name = ps.State("Dollar")


def on_input(payload):
    print("Browser → Python payload:", payload)
    name.set(payload["value"])


heading = ps.Heading(name)

input_box = ps.Input(
    value=name,
    on_input=on_input,
)

app = ps.Column(
    heading,
    input_box,
)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Heading ID:", heading.id)
print("Input ID:", input_box.id)
print("Initial:", name.value)


async def _test_binding():
    import websockets

    async with websockets.connect(url) as ws:
        print("WebSocket connected: PASS")

        event = {
            "type": "event",
            "id": input_box.id,
            "event": "input",
            "payload": {
                "value": "Racit"
            },
        }

        await ws.send(json.dumps(event))

        response = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("Received:", response)

        assert response["type"] == "response"
        assert response["ok"] is True

        update = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("Update:", update)

        assert update["type"] == "update"
        assert update["id"] == heading.id
        assert update["props"]["text"] == "Racit"

        assert name.value == "Racit"

        print("Browser → Python callback: PASS")
        print("Python callback → State.set(): PASS")
        print("State → Heading update: PASS")
        print("Final state:", name.value)

        print()
        print("=== INPUT TWO-WAY BINDING PASS ===")


def test_sync_wrapper():
    asyncio.run(_test_binding())

    server.stop()
