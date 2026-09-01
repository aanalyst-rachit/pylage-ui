from __future__ import annotations

from typing import Any

from pylage.core.diff import DiffOperation
from pylage.core.protocol import (
    TreeAddMessage,
    TreeRemoveMessage,
    TreeReplaceMessage,
    UpdateMessage,
)


PatchMessage = Any


def operation_to_message(operation: DiffOperation) -> PatchMessage:
    """Convert one diff operation into an existing protocol message."""

    if not isinstance(operation, dict):
        raise TypeError("diff operation must be a dictionary")

    operation_type = operation.get("type")

    if operation_type == "update":
        props = operation.get("props", {})
        remove_props = operation.get("remove_props", [])

        if not isinstance(props, dict):
            raise TypeError("update operation props must be a dictionary")

        if not isinstance(remove_props, list):
            raise TypeError(
                "update operation remove_props must be a list"
            )

        if not all(
            isinstance(name, str) and name
            for name in remove_props
        ):
            raise ValueError(
                "update operation remove_props must contain valid names"
            )

        return UpdateMessage(
            component_id=_require_id(operation.get("id"), "update"),
            props=props,
            remove_props=remove_props,
        )

    if operation_type == "insert":
        node = operation.get("node")

        if not isinstance(node, dict):
            raise TypeError("insert operation node must be a dictionary")

        return TreeAddMessage(
            parent_id=_require_id(
                operation.get("parent_id"),
                "insert",
            ),
            components=[node],
            index=_require_index(operation.get("index")),
        )

    if operation_type == "remove":
        return TreeRemoveMessage(
            parent_id=_require_id(
                operation.get("parent_id"),
                "remove",
            ),
            component_ids=[
                _require_id(operation.get("id"), "remove"),
            ],
        )

    if operation_type == "replace":
        node = operation.get("node")

        if not isinstance(node, dict):
            raise TypeError("replace operation node must be a dictionary")

        index = operation.get("index")

        if not isinstance(index, int):
            raise ValueError(
                "replace operation requires a valid index"
            )

        return TreeReplaceMessage(
            parent_id=_require_id(
                operation.get("parent_id"),
                "replace",
            ),
            old_component_id=_require_id(
                operation.get("id"),
                "replace",
            ),
            new_component=node,
            index=index,
        )

    if operation_type == "events":
        raise ValueError(
            "events diff operations do not have a dedicated protocol message"
        )

    raise ValueError(
        f"unsupported diff operation type: {operation_type!r}"
    )


def operations_to_messages(
    operations: list[DiffOperation],
) -> list[PatchMessage]:
    """Convert diff operations to protocol messages deterministically."""

    if not isinstance(operations, list):
        raise TypeError("operations must be a list")

    return [
        operation_to_message(operation)
        for operation in operations
    ]


def operations_to_json(
    operations: list[DiffOperation],
) -> list[str]:
    """Convert diff operations directly into protocol JSON messages."""

    return [
        message.to_json()
        for message in operations_to_messages(operations)
    ]


def _require_id(value: Any, operation_type: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"{operation_type} operation requires a valid id"
        )

    return value


def _require_index(value: Any) -> int | None:
    if value is None:
        return None

    if not isinstance(value, int):
        raise ValueError("operation index must be an integer")

    return value
