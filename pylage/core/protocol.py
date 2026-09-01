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
    remove_props: list[str] | None = None
    prop_meta: dict[str, dict[str, Any]] | None = None

    @property
    def type(self) -> str:
        return "update"

    def to_dict(self) -> dict[str, Any]:
        message: dict[str, Any] = {
            "type": self.type,
            "id": self.component_id,
            "props": self.props,
        }

        if self.remove_props:
            message["remove_props"] = self.remove_props

        if self.prop_meta is not None:
            message["prop_meta"] = self.prop_meta

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
    ) -> "UpdateMessage":
        if not isinstance(data, dict):
            raise TypeError("Update message must be a dictionary.")

        if data.get("type") != "update":
            raise ValueError("Invalid update message type.")

        component_id = data.get("id")
        props = data.get("props")
        remove_props = data.get("remove_props", [])
        prop_meta = data.get("prop_meta")

        if not isinstance(component_id, str) or not component_id:
            raise ValueError("Update message requires a valid id.")

        if not isinstance(props, dict):
            raise ValueError("Update message requires props.")

        if not isinstance(remove_props, list):
            raise ValueError(
                "Update message remove_props must be a list."
            )

        if not all(
            isinstance(name, str) and name
            for name in remove_props
        ):
            raise ValueError(
                "Update message remove_props must contain valid names."
            )

        if prop_meta is not None and not isinstance(prop_meta, dict):
            raise ValueError(
                "Update message prop_meta must be a dictionary."
            )

        return cls(
            component_id=component_id,
            props=props,
            remove_props=remove_props,
            prop_meta=prop_meta,
        )

    @classmethod
    def from_json(cls, data: str) -> "UpdateMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON update message."
            ) from exc

        return cls.from_dict(decoded)

@dataclass(frozen=True)
class TreeAddMessage:
    """Server-to-client message describing newly added components."""

    parent_id: str
    components: list[dict[str, Any]]
    index: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.parent_id, str) or not self.parent_id:
            raise ValueError(
                "Tree add message requires a valid parent_id."
            )

        if not isinstance(self.components, list):
            raise ValueError(
                "Tree add message requires components."
            )

        if self.index is not None and not isinstance(self.index, int):
            raise ValueError(
                "Tree add message index must be an integer."
            )

    @property
    def type(self) -> str:
        return "tree_add"

    def to_dict(self) -> dict[str, Any]:
        data = {
            "type": self.type,
            "parent_id": self.parent_id,
            "components": self.components,
        }

        if self.index is not None:
            data["index"] = self.index

        return data

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "TreeAddMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree add message must be a dictionary."
            )

        if data.get("type") != "tree_add":
            raise ValueError(
                "Invalid tree add message type."
            )

        parent_id = data.get("parent_id")
        components = data.get("components")
        index = data.get("index")

        if not isinstance(parent_id, str) or not parent_id:
            raise ValueError(
                "Tree add message requires a valid parent_id."
            )

        if not isinstance(components, list):
            raise ValueError(
                "Tree add message requires components."
            )

        if index is not None and not isinstance(index, int):
            raise ValueError(
                "Tree add message index must be an integer."
            )

        return cls(
            parent_id=parent_id,
            components=components,
            index=index,
        )

    @classmethod
    def from_json(cls, data: str) -> "TreeAddMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree add message."
            ) from exc

        return cls.from_dict(decoded)



@dataclass(frozen=True)
class TreeMoveMessage:
    """Server-to-client message describing a component move."""

    component_id: str
    old_parent_id: str
    new_parent_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.component_id, str) or not self.component_id:
            raise ValueError(
                "Tree move message requires a valid component_id."
            )

        if not isinstance(self.old_parent_id, str) or not self.old_parent_id:
            raise ValueError(
                "Tree move message requires a valid old_parent_id."
            )

        if not isinstance(self.new_parent_id, str) or not self.new_parent_id:
            raise ValueError(
                "Tree move message requires a valid new_parent_id."
            )

    @property
    def type(self) -> str:
        return "tree_move"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "component_id": self.component_id,
            "old_parent_id": self.old_parent_id,
            "new_parent_id": self.new_parent_id,
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
    ) -> "TreeMoveMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree move message must be a dictionary."
            )

        if data.get("type") != "tree_move":
            raise ValueError(
                "Invalid tree move message type."
            )

        return cls(
            component_id=data.get("component_id"),
            old_parent_id=data.get("old_parent_id"),
            new_parent_id=data.get("new_parent_id"),
        )

    @classmethod
    def from_json(cls, data: str) -> "TreeMoveMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree move message."
            ) from exc

        return cls.from_dict(decoded)


@dataclass(frozen=True)
class TreeReplaceMessage:
    """Server-to-client message replacing one component in the tree."""

    parent_id: str
    old_component_id: str
    new_component: dict[str, Any]
    index: int

    def __post_init__(self) -> None:
        if not isinstance(self.parent_id, str) or not self.parent_id:
            raise ValueError(
                "Tree replace message requires a valid parent_id."
            )

        if (
            not isinstance(self.old_component_id, str)
            or not self.old_component_id
        ):
            raise ValueError(
                "Tree replace message requires a valid old_component_id."
            )

        if not isinstance(self.new_component, dict):
            raise TypeError(
                "Tree replace message requires new_component."
            )

        if not isinstance(self.index, int):
            raise TypeError(
                "Tree replace message requires an integer index."
            )

    @property
    def type(self) -> str:
        return "tree_replace"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "parent_id": self.parent_id,
            "old_component_id": self.old_component_id,
            "new_component": self.new_component,
            "index": self.index,
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
    ) -> "TreeReplaceMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree replace message must be a dictionary."
            )

        if data.get("type") != "tree_replace":
            raise ValueError(
                "Invalid tree replace message type."
            )

        return cls(
            parent_id=data.get("parent_id"),
            old_component_id=data.get("old_component_id"),
            new_component=data.get("new_component"),
            index=data.get("index"),
        )

    @classmethod
    def from_json(cls, data: str) -> "TreeReplaceMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree replace message."
            ) from exc

        return cls.from_dict(decoded)


@dataclass(frozen=True)
class TreeSetChildrenMessage:
    """Server-to-client message replacing a component's children."""

    parent_id: str
    children: list[dict[str, Any]]

    def __post_init__(self) -> None:
        if not isinstance(self.parent_id, str) or not self.parent_id:
            raise ValueError(
                "Tree set-children message requires a valid parent_id."
            )

        if not isinstance(self.children, list):
            raise TypeError(
                "Tree set-children message requires children."
            )

        if not all(isinstance(child, dict) for child in self.children):
            raise TypeError(
                "Tree set-children message requires child dictionaries."
            )

    @property
    def type(self) -> str:
        return "tree_set_children"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "parent_id": self.parent_id,
            "children": list(self.children),
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
    ) -> "TreeSetChildrenMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree set-children message must be a dictionary."
            )

        if data.get("type") != "tree_set_children":
            raise ValueError(
                "Invalid tree set-children message type."
            )

        return cls(
            parent_id=data.get("parent_id"),
            children=data.get("children"),
        )

    @classmethod
    def from_json(
        cls,
        data: str,
    ) -> "TreeSetChildrenMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree set-children message."
            ) from exc

        return cls.from_dict(decoded)


@dataclass(frozen=True)
class TreeClearMessage:
    """Server-to-client message clearing all children of a component."""

    parent_id: str
    component_ids: list[str]

    def __post_init__(self) -> None:
        if not isinstance(self.parent_id, str) or not self.parent_id:
            raise ValueError(
                "Tree clear message requires a valid parent_id."
            )

        if not isinstance(self.component_ids, list):
            raise TypeError(
                "Tree clear message requires component_ids."
            )

        if not all(
            isinstance(component_id, str) and component_id
            for component_id in self.component_ids
        ):
            raise ValueError(
                "Tree clear message requires valid component ids."
            )

    @property
    def type(self) -> str:
        return "tree_clear"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "parent_id": self.parent_id,
            "component_ids": list(self.component_ids),
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
    ) -> "TreeClearMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree clear message must be a dictionary."
            )

        if data.get("type") != "tree_clear":
            raise ValueError(
                "Invalid tree clear message type."
            )

        return cls(
            parent_id=data.get("parent_id"),
            component_ids=data.get("component_ids"),
        )

    @classmethod
    def from_json(cls, data: str) -> "TreeClearMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree clear message."
            ) from exc

        return cls.from_dict(decoded)


@dataclass(frozen=True)
class TreeRemoveMessage:
    """Server-to-client message describing removed components."""

    parent_id: str
    component_ids: list[str]

    def __post_init__(self) -> None:
        if not isinstance(self.parent_id, str) or not self.parent_id:
            raise ValueError(
                "Tree remove message requires a valid parent_id."
            )

        if not isinstance(self.component_ids, list):
            raise ValueError(
                "Tree remove message requires component_ids."
            )

        if not all(
            isinstance(component_id, str) and component_id
            for component_id in self.component_ids
        ):
            raise ValueError(
                "Tree remove message requires valid component_ids."
            )

    @property
    def type(self) -> str:
        return "tree_remove"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "parent_id": self.parent_id,
            "component_ids": self.component_ids,
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
    ) -> "TreeRemoveMessage":
        if not isinstance(data, dict):
            raise TypeError(
                "Tree remove message must be a dictionary."
            )

        if data.get("type") != "tree_remove":
            raise ValueError(
                "Invalid tree remove message type."
            )

        parent_id = data.get("parent_id")
        component_ids = data.get("component_ids")

        if not isinstance(parent_id, str) or not parent_id:
            raise ValueError(
                "Tree remove message requires a valid parent_id."
            )

        if not isinstance(component_ids, list):
            raise ValueError(
                "Tree remove message requires component_ids."
            )

        return cls(
            parent_id=parent_id,
            component_ids=component_ids,
        )

    @classmethod
    def from_json(cls, data: str) -> "TreeRemoveMessage":
        try:
            decoded = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON tree remove message."
            ) from exc

        return cls.from_dict(decoded)
