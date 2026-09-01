from __future__ import annotations

import copy
import json
from typing import Any

from pylage.core.component import Component
from pylage.core.registry import registry
from pylage.core.state import State


def _snapshot_value(value: Any) -> Any:
    """Convert a value into an immutable-at-snapshot-time JSON-safe value."""

    if isinstance(value, State):
        return _snapshot_value(value.value)

    if isinstance(value, dict):
        return {
            _snapshot_value(key): _snapshot_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [_snapshot_value(item) for item in value]

    if isinstance(value, set):
        return [
            _snapshot_value(item)
            for item in sorted(value, key=repr)
        ]

    try:
        copied = copy.deepcopy(value)
    except Exception as exc:
        raise TypeError(
            f"Snapshot value of type {type(value).__name__} "
            "is not serializable."
        ) from exc

    try:
        json.dumps(copied)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"Snapshot value of type {type(value).__name__} "
            "is not JSON serializable."
        ) from exc

    return copied


def component_to_snapshot(
    component: Component,
) -> dict[str, Any]:
    """Create a stable, JSON-serializable snapshot of a Component tree."""

    if not isinstance(component, Component):
        raise TypeError(
            "component_to_snapshot expects a Component."
        )

    definition = registry.get(component.type)

    snapshot = {
        "id": component.id,
        "type": component.type,
        "tag": (
            definition.tag
            if definition is not None
            else "div"
        ),
        "events": ",".join(component.events.keys()),
        "props": {
            key: _snapshot_value(value)
            for key, value in component.props.items()
        },
        "children": [
            component_to_snapshot(child)
            for child in component.children
            if isinstance(child, Component)
        ],
    }

    # Final contract guard: every public snapshot must be JSON serializable.
    try:
        json.dumps(snapshot)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Component snapshot must be JSON serializable."
        ) from exc

    return snapshot
