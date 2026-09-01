from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


@dataclass(frozen=True)
class EventMessage:
    """Client-to-server UI event message."""

    component_id: str
    event: str
    payload: Any = None

    @property
    def type(self) -> str:
        return "event"

    def to_dict(self) -> dict[str, Any]:
        message: dict[str, Any] = {
            "type": self.type,
            "id": self.component_id,
            "event": self.event,
        }

        if self.payload is not None:
            message["payload"] = self.payload

        return message

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "EventMessage":
        if not isinstance(data, dict):
            raise TypeError("Event message must be a dictionary.")

        if data.get("type") != "event":
            raise ValueError("Invalid event message type.")

        component_id = data.get("id")
        event = data.get("event")

        if not isinstance(component_id, str) or not component_id:
            raise ValueError("Event message requires a valid id.")

        if not isinstance(event, str) or not event:
            raise ValueError("Event message requires a valid event.")

        return cls(
            component_id=component_id,
            event=event,
            payload=data.get("payload"),
        )

    @classmethod
    def from_json(cls, data: str) -> "EventMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON event message.") from exc

        return cls.from_dict(decoded)


@dataclass(frozen=True)
class UpdateMessage:
    """Server-to-client component update message."""

    component_id: str
    props: dict[str, Any]

    @property
    def type(self) -> str:
        return "update"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "id": self.component_id,
            "props": self.props,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "UpdateMessage":
        if not isinstance(data, dict):
            raise TypeError("Update message must be a dictionary.")

        if data.get("type") != "update":
            raise ValueError("Invalid update message type.")

        component_id = data.get("id")
        props = data.get("props")

        if not isinstance(component_id, str) or not component_id:
            raise ValueError("Update message requires a valid id.")

        if not isinstance(props, dict):
            raise ValueError("Update message requires props.")

        return cls(
            component_id=component_id,
            props=props,
        )

    @classmethod
    def from_json(cls, data: str) -> "UpdateMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON update message.") from exc

        return cls.from_dict(decoded)
