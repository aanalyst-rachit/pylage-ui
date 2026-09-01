import asyncio
import json

from websockets.asyncio.client import connect

import pylage as ps
from pylage.runtime.websocket import WebSocketServer


print("=== PYLAGE WEBSOCKET TEST ===")


calls = []


def clicked():
    calls.append("clicked")
    return "handler-ok"


button = ps.Button(
    "Click me",
    on_click=clicked,
)

app = ps.Column(button)

server = WebSocketServer(app)

url = server.start()

print("URL:", url)
print("Running:", server.running)

assert server.running


async def _test_connection():
    async with connect(url) as websocket:
        message = {
            "type": "event",
            "id": button.id,
            "event": "click",
        }

        await websocket.send(json.dumps(message))

        raw_response = await websocket.recv()

        print("Response:", raw_response)

        response = json.loads(raw_response)

        assert response["type"] == "response"
        assert response["ok"] is True
        assert response["result"] == "handler-ok"


asyncio.run(_test_connection())

print("Calls:", calls)

assert calls == ["clicked"]

server.stop()

print("Running after stop:", server.running)

assert not server.running

print("=== WEBSOCKET PASS ===")
