import asyncio
import json

import pylage as ps
from pylage.runtime.websocket import WebSocketServer


def test_websocket_state_update_uses_reactive_pipeline():
    async def run():
        count = ps.State(0)

        heading = ps.Heading(text=count)
        app = ps.Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                count.set(1)

                raw = await asyncio.wait_for(
                    ws.recv(),
                    timeout=2,
                )

                message = json.loads(raw)

                assert message["type"] == "update"
                assert message["id"] == heading.id
                assert message["props"]["text"] == 1

        finally:
            server.stop()

    asyncio.run(run())

def test_websocket_batches_multiple_state_changes_into_one_final_update():
    async def run():
        count = ps.State(0)

        heading = ps.Heading(text=count)
        app = ps.Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                count.set(1)
                count.set(2)
                count.set(3)

                raw = await asyncio.wait_for(
                    ws.recv(),
                    timeout=2,
                )

                message = json.loads(raw)

                assert message["type"] == "update"
                assert message["id"] == heading.id
                assert message["props"]["text"] == 3

                # There must not be another update for the same
                # synchronous State-change batch.
                try:
                    extra = await asyncio.wait_for(
                        ws.recv(),
                        timeout=0.15,
                    )
                except asyncio.TimeoutError:
                    extra = None

                assert extra is None

        finally:
            server.stop()

    asyncio.run(run())
