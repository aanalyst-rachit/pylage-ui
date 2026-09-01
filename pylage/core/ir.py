from __future__ import annotations

import copy
from typing import Any
from pylage.core.registry import registry
from pylage.core.state import State


def _copy_ir_value(value: Any) -> Any:
    """Deep-copy compiler values while preserving runtime State identity."""

    if isinstance(value, State):
        return value

    if isinstance(value, dict):
        return {
            key: _copy_ir_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _copy_ir_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _copy_ir_value(item)
            for item in value
        )

    if isinstance(value, set):
        return {
            _copy_ir_value(item)
            for item in value
        }

    return copy.deepcopy(value)


class IRNode:
    """Minimal compiler-layer intermediate representation node."""

    VALID_NODE_TYPES = {"component"}

    def __init__(
        self,
        node_id: str,
        node_type: str,
        component_id: str | None = None,
        props: dict[str, Any] | None = None,
        children: list["IRNode"] | None = None,
        style_ref: Any = None,
    ) -> None:
        self._validate_node_id(node_id)
        self._validate_node_type(node_type)
        self._validate_component_id(component_id, node_type)
        self._validate_props(props)
        self._validate_children(children)

        self.node_id = node_id
        self.node_type = node_type
        self.component_id = component_id
        self.props = _copy_ir_value(props) if props is not None else {}
        self.children = list(children) if children is not None else []
        self.style_ref = style_ref

    @staticmethod
    def _validate_node_id(node_id: str) -> None:
        if not isinstance(node_id, str) or not node_id:
            raise ValueError("node_id must be a non-empty string")

    @classmethod
    def _validate_node_type(cls, node_type: str) -> None:
        if node_type not in cls.VALID_NODE_TYPES:
            raise ValueError(
                f"Invalid node_type: {node_type!r}. "
                f"Must be one of: {cls.VALID_NODE_TYPES}"
            )

    @staticmethod
    def _validate_component_id(
        component_id: str | None,
        node_type: str,
    ) -> None:
        if node_type == "component":
            if not isinstance(component_id, str) or not component_id:
                raise ValueError(
                    "component_id must be a non-empty string "
                    "for component nodes"
                )

    @staticmethod
    def _validate_props(
        props: dict[str, Any] | None,
    ) -> None:
        if props is not None and not isinstance(props, dict):
            raise ValueError("props must be a dictionary or None")

    @staticmethod
    def _validate_children(
        children: list["IRNode"] | None,
    ) -> None:
        if children is None:
            return

        if not isinstance(children, list):
            raise ValueError("children must be a list or None")

        for child in children:
            if not isinstance(child, IRNode):
                raise ValueError(
                    "All children must be IRNode instances"
                )

    def add_child(self, child: "IRNode") -> None:
        """Append one IR child while preserving insertion order."""

        if not isinstance(child, IRNode):
            raise ValueError("Child must be an IRNode instance")

        self.children.append(child)

    def __repr__(self) -> str:
        return (
            "IRNode("
            f"node_id={self.node_id!r}, "
            f"node_type={self.node_type!r}, "
            f"component_id={self.component_id!r}, "
            f"props={self.props!r}, "
            f"style_ref={self.style_ref!r}, "
            f"children={self.children!r}"
            ")"
        )


def snapshot_to_ir(snapshot: dict[str, Any]) -> IRNode:
    """Convert a PyLage snapshot into compiler-layer IR."""

    if not isinstance(snapshot, dict):
        raise TypeError("snapshot must be a dictionary")

    if "id" not in snapshot:
        raise ValueError("snapshot must contain 'id'")

    if "type" not in snapshot:
        raise ValueError("snapshot must contain 'type'")

    node_id = snapshot["id"]
    component_id = snapshot["type"]

    props = snapshot.get("props", {})
    children = snapshot.get("children", [])

    if not isinstance(children, list):
        raise ValueError("snapshot children must be a list")

    ir_children = [
        snapshot_to_ir(child)
        for child in children
    ]

    return IRNode(
        node_id=node_id,
        node_type="component",
        component_id=component_id,
        props=copy.deepcopy(props),
        children=ir_children,
        style_ref=None,
    )

def normalize_ir(node: IRNode) -> IRNode:
    """Return a canonical compiler-layer copy of an IR tree.

    Normalization is intentionally compiler-only. It preserves component
    identity, node identity, child ordering, and opaque style references
    without evaluating runtime state, rendering styles, or consulting
    runtime dependency/diff/patch systems.
    """

    if not isinstance(node, IRNode):
        raise TypeError("node must be an IRNode")

    normalized_children = [
        normalize_ir(child)
        for child in node.children
    ]

    return IRNode(
        node_id=node.node_id,
        node_type=node.node_type,
        component_id=node.component_id,
        props=copy.deepcopy(node.props),
        children=normalized_children,
        style_ref=copy.deepcopy(node.style_ref),
    )

def analyze_ir(node: IRNode) -> dict[str, Any]:
    """Perform lightweight static analysis of an IR tree.

    The analyzer is compiler-only. It does not evaluate runtime state,
    resolve styles, execute events, or mutate the supplied IR tree.
    """

    if not isinstance(node, IRNode):
        raise TypeError("node must be an IRNode")

    seen_node_ids: set[str] = set()
    ordered_node_ids: list[str] = []
    component_ids: list[str] = []
    duplicate_node_ids: list[str] = []
    total_nodes = 0

    def visit(current: IRNode) -> None:
        nonlocal total_nodes

        if not isinstance(current, IRNode):
            raise TypeError("IR tree contains a non-IRNode child")

        total_nodes += 1

        if current.node_id in seen_node_ids:
            if current.node_id not in duplicate_node_ids:
                duplicate_node_ids.append(current.node_id)
        else:
            seen_node_ids.add(current.node_id)
            ordered_node_ids.append(current.node_id)

        if current.component_id is not None:
            component_ids.append(current.component_id)

        for child in current.children:
            visit(child)

    visit(node)

    return {
        "total_nodes": total_nodes,
        "node_ids": ordered_node_ids,
        "component_ids": component_ids,
        "duplicate_node_ids": duplicate_node_ids,
        "is_valid": not duplicate_node_ids,
    }

def validate_ir(node: IRNode) -> None:
    """Validate the structural integrity of an IR tree.

    Validation is compiler-only and does not mutate the supplied tree or
    evaluate runtime state, styles, dependencies, or events.
    """

    if not isinstance(node, IRNode):
        raise TypeError("node must be an IRNode")

    seen_node_ids: set[str] = set()

    def visit(current: IRNode) -> None:
        if not isinstance(current, IRNode):
            raise TypeError("IR tree contains a non-IRNode child")

        if current.node_id in seen_node_ids:
            raise ValueError(
                f"Duplicate IR node_id: {current.node_id!r}"
            )

        seen_node_ids.add(current.node_id)

        if current.node_type not in IRNode.VALID_NODE_TYPES:
            raise ValueError(
                f"Invalid IR node_type: {current.node_type!r}"
            )

        if current.node_type == "component":
            if (
                not isinstance(current.component_id, str)
                or not current.component_id
            ):
                raise ValueError(
                    "Component IR nodes require a non-empty "
                    "component_id"
                )

        if not isinstance(current.props, dict):
            raise ValueError(
                f"IR node {current.node_id!r} has invalid props"
            )

        if not isinstance(current.children, list):
            raise ValueError(
                f"IR node {current.node_id!r} has invalid children"
            )

        for child in current.children:
            visit(child)

    visit(node)



def constant_fold(value: Any) -> Any:
    """Fold compiler-safe constant expressions without touching runtime state."""

    if isinstance(value, State):
        return value

    if not isinstance(value, tuple) or len(value) != 3:
        return copy.deepcopy(value)

    operator, left, right = value

    if operator not in {"add", "sub", "mul", "div"}:
        return copy.deepcopy(value)

    left = constant_fold(left)
    right = constant_fold(right)

    if not isinstance(left, (int, float)) or isinstance(left, bool):
        return (operator, left, right)

    if not isinstance(right, (int, float)) or isinstance(right, bool):
        return (operator, left, right)

    if operator == "add":
        return left + right
    if operator == "sub":
        return left - right
    if operator == "mul":
        return left * right
    if operator == "div":
        if right == 0:
            return (operator, left, right)
        return left / right

    return (operator, left, right)

def analyze_ir_dependencies(node: IRNode) -> dict[str, Any]:
    """Analyze reactive prop dependencies in an IR tree."""

    if not isinstance(node, IRNode):
        raise TypeError("node must be an IRNode")

    node_ids: list[str] = []
    dependencies: list[dict[str, str]] = []

    def visit(current: IRNode) -> None:
        node_ids.append(current.node_id)

        definition = registry.get(current.component_id)

        for prop_name in current.props:
            if definition is None or definition.props is None:
                reactive = True
            else:
                prop_definition = definition.props.get(prop_name)
                reactive = (
                    True
                    if prop_definition is None
                    else prop_definition.reactive
                )

            if reactive:
                dependencies.append({
                    "node_id": current.node_id,
                    "prop_name": prop_name,
                })

        for child in current.children:
            visit(child)

    visit(node)

    return {
        "node_ids": node_ids,
        "dependencies": dependencies,
    }

def plan_patches(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """Plan patch operations from two snapshots."""
    from pylage.core.diff import diff

    return diff(previous, current)

def optimize_ir(node: IRNode) -> IRNode:
    """Return an optimized compiler-layer copy of an IR tree.

    Optimization is compiler-only. It preserves node identity, structure,
    child ordering, and opaque style references while applying safe
    constant folding to IR prop values.
    """

    if not isinstance(node, IRNode):
        raise TypeError("node must be an IRNode")

    optimized_props = {
        name: constant_fold(value)
        for name, value in node.props.items()
    }

    optimized_children = [
        optimize_ir(child)
        for child in node.children
    ]

    return IRNode(
        node_id=node.node_id,
        node_type=node.node_type,
        component_id=node.component_id,
        props=optimized_props,
        children=optimized_children,
        style_ref=copy.deepcopy(node.style_ref),
    )
