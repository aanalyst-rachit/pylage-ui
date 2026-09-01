from __future__ import annotations

from typing import Any


DiffOperation = dict[str, Any]


def diff(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> list[DiffOperation]:
    """Calculate deterministic minimal operations between two snapshots."""

    if not isinstance(previous, dict):
        raise TypeError("previous snapshot must be a dict")

    if not isinstance(current, dict):
        raise TypeError("current snapshot must be a dict")

    operations: list[DiffOperation] = []
    _diff_node(previous, current, operations)
    return operations


def _diff_node(
    previous: dict[str, Any],
    current: dict[str, Any],
    operations: list[DiffOperation],
    *,
    parent_id: Any = None,
    index: int | None = None,
) -> None:
    previous_id = previous.get("id")
    current_id = current.get("id")

    if previous_id != current_id:
        operation = {
            "type": "replace",
            "id": previous_id,
            "node": current,
        }

        if parent_id is not None:
            operation["parent_id"] = parent_id

        if index is not None:
            operation["index"] = index

        operations.append(operation)
        return

    if previous.get("type") != current.get("type"):
        operation = {
            "type": "replace",
            "id": current_id,
            "node": current,
        }

        if parent_id is not None:
            operation["parent_id"] = parent_id

        if index is not None:
            operation["index"] = index

        operations.append(operation)
        return

    previous_props = previous.get("props", {})
    current_props = current.get("props", {})

    changed_props: dict[str, Any] = {}
    removed_props: list[str] = []

    for name, value in current_props.items():
        if name not in previous_props or previous_props[name] != value:
            changed_props[name] = value

    for name in previous_props:
        if name not in current_props:
            removed_props.append(name)

    if changed_props or removed_props:
        operations.append(
            {
                "type": "update",
                "id": current_id,
                "props": changed_props,
                "remove_props": removed_props,
            }
        )

    if previous.get("events") != current.get("events"):
        operations.append(
            {
                "type": "events",
                "id": current_id,
                "events": current.get("events", ""),
            }
        )

    _diff_children(
        current_id,
        previous.get("children", []),
        current.get("children", []),
        operations,
    )


def _diff_children(
    parent_id: Any,
    previous_children: list[dict[str, Any]],
    current_children: list[dict[str, Any]],
    operations: list[DiffOperation],
) -> None:
    previous_by_id = {
        child.get("id"): child
        for child in previous_children
    }

    current_by_id = {
        child.get("id"): child
        for child in current_children
    }

    # Removed nodes are emitted in previous-tree order.
    for index, child in enumerate(previous_children):
        child_id = child.get("id")

        if child_id not in current_by_id:
            operations.append(
                {
                    "type": "remove",
                    "parent_id": parent_id,
                    "id": child_id,
                    "index": index,
                }
            )

    # Current-tree order determines insertion/update order.
    for index, child in enumerate(current_children):
        child_id = child.get("id")

        if child_id not in previous_by_id:
            operations.append(
                {
                    "type": "insert",
                    "parent_id": parent_id,
                    "index": index,
                    "node": child,
                }
            )
            continue

        _diff_node(
            previous_by_id[child_id],
            child,
            operations,
            parent_id=parent_id,
            index=index,
        )
