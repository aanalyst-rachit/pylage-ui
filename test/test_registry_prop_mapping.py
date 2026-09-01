import pytest
import asyncio
import json

import pylage as ps
from pylage.core.component import Component
from pylage.runtime.websocket import WebSocketServer

print("=== PYLAGE REGISTRY PROP MAPPING TEST ===")

class_name = ps.State("primary")
disabled = ps.State(False)
title = ps.State("Initial")

component = Component(
    type="Button",
    props={
        "text": "Save",
        "class_name": class_name,
        "disabled": disabled,
        "title": title,
    },
)

app = ps.Column(component)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Component ID:", component.id)


@pytest.mark.asyncio
async def test_mapping():
    import websockets

    async with websockets.connect(url) as ws:
        print("WebSocket connected: PASS")

        class_name.set("danger")

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("class_name update:", message)

        assert message["type"] == "update"
        assert message["id"] == component.id

        assert message["props"]["class_name"] == "danger"

        assert message["prop_meta"]["class_name"] == {
            "kind": "attribute",
            "html_name": "class",
        }

        print("class_name → class metadata: PASS")

        disabled.set(True)

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        assert message["props"]["disabled"] is True

        assert message["prop_meta"]["disabled"] == {
            "kind": "boolean",
            "html_name": "disabled",
        }

        print("disabled boolean metadata: PASS")

        title.set("Updated title")

        message = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        assert message["props"]["title"] == "Updated title"

        assert message["prop_meta"]["title"] == {
            "kind": "attribute",
            "html_name": "title",
        }

        print("title attribute metadata: PASS")

        print()
        print("=== REGISTRY PROP MAPPING TEST PASS ===")


