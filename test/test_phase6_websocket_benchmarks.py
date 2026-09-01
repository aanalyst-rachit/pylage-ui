import asyncio
import json
import time

import pylage as ps
from pylage.runtime.websocket import WebSocketServer


def test_phase6_websocket_state_update_latency():
    async def run():
        count = ps.State(0)
        heading = ps.Heading(text=count)
        app = ps.Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                samples = 100

                start = time.perf_counter()

                for value in range(1, samples + 1):
                    count.set(value)

                    raw = await asyncio.wait_for(
                        ws.recv(),
                        timeout=2,
                    )

                    message = json.loads(raw)

                    assert message["type"] == "update"
                    assert message["id"] == heading.id
                    assert message["props"]["text"] == value

                elapsed = time.perf_counter() - start

                print("\n===== PHASE 6 — WEBSOCKET STATE UPDATE =====")
                print(f"iterations        : {samples}")
                print(f"total             : {elapsed:.9f}s")
                print(f"per update        : {elapsed / samples:.9f}s")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_tree_patch_latency():
    async def run():
        root = ps.Column()
        server = WebSocketServer(root)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                samples = 100

                start = time.perf_counter()

                for index in range(samples):
                    child = ps.Heading(text=f"item-{index}")
                    root.add(child)

                    raw = await asyncio.wait_for(
                        ws.recv(),
                        timeout=2,
                    )

                    message = json.loads(raw)

                    assert message["type"] == "tree_add"
                    assert message["parent_id"] == root.id

                elapsed = time.perf_counter() - start

                print("\n===== PHASE 6 — WEBSOCKET TREE PATCH =====")
                print(f"iterations        : {samples}")
                print(f"total             : {elapsed:.9f}s")
                print(f"per patch         : {elapsed / samples:.9f}s")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_multi_client_broadcast():
    async def run():
        count = ps.State(0)
        heading = ps.Heading(text=count)
        app = ps.Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            client_count = 10

            connections = [
                await websockets.connect(url)
                for _ in range(client_count)
            ]

            try:
                start = time.perf_counter()

                count.set(1)

                messages = await asyncio.gather(
                    *[
                        asyncio.wait_for(
                            ws.recv(),
                            timeout=2,
                        )
                        for ws in connections
                    ]
                )

                elapsed = time.perf_counter() - start

                for raw in messages:
                    message = json.loads(raw)

                    assert message["type"] == "update"
                    assert message["id"] == heading.id
                    assert message["props"]["text"] == 1

                print("\n===== PHASE 6 — WEBSOCKET BROADCAST =====")
                print(f"clients            : {client_count}")
                print(f"total              : {elapsed:.9f}s")
                print(f"per client         : {elapsed / client_count:.9f}s")

            finally:
                await asyncio.gather(
                    *(ws.close() for ws in connections)
                )

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_client_scaling():
    async def run():
        for client_count in (10, 50, 100):
            count = ps.State(0)
            heading = ps.Heading(text=count)
            app = ps.Column(heading)

            server = WebSocketServer(app)

            try:
                url = server.start()

                import websockets

                connections = [
                    await websockets.connect(url)
                    for _ in range(client_count)
                ]

                try:
                    start = time.perf_counter()

                    count.set(1)

                    messages = await asyncio.gather(
                        *[
                            asyncio.wait_for(
                                ws.recv(),
                                timeout=5,
                            )
                            for ws in connections
                        ]
                    )

                    elapsed = time.perf_counter() - start

                    assert len(messages) == client_count

                    for raw in messages:
                        message = json.loads(raw)
                        assert message["type"] == "update"
                        assert message["id"] == heading.id
                        assert message["props"]["text"] == 1

                    print("\n===== PHASE 6 — WEBSOCKET CLIENT SCALING =====")
                    print(f"clients            : {client_count}")
                    print(f"total              : {elapsed:.9f}s")
                    print(f"per client         : {elapsed / client_count:.9f}s")

                finally:
                    await asyncio.gather(
                        *(ws.close() for ws in connections)
                    )

            finally:
                server.stop()

    asyncio.run(run())
