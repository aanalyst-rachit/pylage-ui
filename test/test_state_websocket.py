import asyncio
import json

import pylage as ps

from pylage.runtime.websocket import WebSocketServer


async def main():
    count = ps.State(0)

    app = ps.Column(
        ps.Heading(text=count),
    )

    server = WebSocketServer(app)

    try:
        url = server.start()

        print("=== PYLAGE STATE WEBSOCKET TEST ===")
        print("URL:", url)

        import websockets

        async with websockets.connect(url) as ws:
            print("Connected: PASS")

            count.set(1)

            raw = await asyncio.wait_for(
                ws.recv(),
                timeout=2,
            )

            print("Received:", raw)

            message = json.loads(raw)

            assert message["type"] == "update"
            assert message["id"] == app.children[0].id
            assert message["props"]["text"] == 1

            print("Update type: PASS")
            print("Component ID: PASS")
            print("Updated value: PASS")
            print("=== STATE WEBSOCKET PASS ===")

    finally:
        server.stop()


asyncio.run(main())
