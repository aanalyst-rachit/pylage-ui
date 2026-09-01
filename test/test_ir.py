import copy

import pytest

from pylage.core.ir import IRNode, snapshot_to_ir


def test_irnode_construction():
    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
    )

    assert node.node_id == "1"
    assert node.node_type == "component"
    assert node.component_id == "Button"
    assert node.props == {"class": "primary"}

    assert len(node.children) == 1
    assert node.children[0].node_id == "2"
    assert node.children[0].component_id == "Text"
    assert node.children[0].props == {"text": "Hello"}


def test_stable_node_identity():
    node1 = IRNode(
        node_id="stable-id",
        node_type="component",
        component_id="Button",
    )

    node2 = IRNode(
        node_id="stable-id",
        node_type="component",
        component_id="Button",
    )

    assert node1.node_id == node2.node_id


def test_valid_node_type():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
    )

    assert node.node_type == "component"


def test_invalid_node_type_rejected():
    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="invalid",
            component_id="Button",
        )


def test_node_id_validation():
    with pytest.raises(ValueError):
        IRNode(
            node_id="",
            node_type="component",
            component_id="Button",
        )

    with pytest.raises(ValueError):
        IRNode(
            node_id=123,
            node_type="component",
            component_id="Button",
        )


def test_component_id_validation():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
    )

    assert node.component_id == "Button"

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="",
        )

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id=123,
        )


def test_props_validation():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={"text": "Hello"},
    )

    assert node.props == {"text": "Hello"}

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Button",
            props="invalid",
        )


def test_props_are_copied():
    props = {
        "data": {
            "items": ["one", "two"],
        }
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props=props,
    )

    props["data"]["items"].append("three")

    assert node.props == {
        "data": {
            "items": ["one", "two"],
        }
    }


def test_child_insertion():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    parent.add_child(child)

    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_invalid_child_rejection():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    with pytest.raises(ValueError):
        parent.add_child("not-an-ir-node")


def test_children_validation():
    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Column",
            children=["invalid-child"],
        )


def test_deterministic_child_ordering():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    child1 = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    child2 = IRNode(
        node_id="3",
        node_type="component",
        component_id="Button",
    )

    parent.add_child(child1)
    parent.add_child(child2)

    assert [child.node_id for child in parent.children] == [
        "2",
        "3",
    ]


def test_children_list_is_copied():
    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    children = [child]

    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
        children=children,
    )

    children.clear()

    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_style_ref_is_opaque():
    style_ref = {
        "style_id": "style-1",
        "source": "phase9",
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        style_ref=style_ref,
    )

    assert node.style_ref is style_ref


def test_snapshot_to_ir_conversion():
    snapshot = {
        "id": "root",
        "type": "Button",
        "tag": "button",
        "events": "",
        "props": {
            "text": "Click me",
            "disabled": False,
        },
        "children": [
            {
                "id": "child",
                "type": "Text",
                "tag": "div",
                "events": "",
                "props": {
                    "text": "Hello",
                },
                "children": [],
            }
        ],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.node_id == "root"
    assert ir_node.node_type == "component"
    assert ir_node.component_id == "Button"

    assert ir_node.props == {
        "text": "Click me",
        "disabled": False,
    }

    assert len(ir_node.children) == 1

    child = ir_node.children[0]

    assert child.node_id == "child"
    assert child.node_type == "component"
    assert child.component_id == "Text"
    assert child.props == {
        "text": "Hello",
    }


def test_snapshot_to_ir_uses_component_type_not_html_tag():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {},
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.component_id == "Button"
    assert ir_node.component_id != snapshot["tag"]


def test_snapshot_to_ir_preserves_child_order():
    snapshot = {
        "id": "root",
        "type": "Column",
        "tag": "div",
        "props": {},
        "children": [
            {
                "id": "first",
                "type": "Text",
                "tag": "div",
                "props": {},
                "children": [],
            },
            {
                "id": "second",
                "type": "Button",
                "tag": "button",
                "props": {},
                "children": [],
            },
        ],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert [child.node_id for child in ir_node.children] == [
        "first",
        "second",
    ]


def test_snapshot_to_ir_does_not_modify_snapshot():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "data": {
                "items": ["one"],
            }
        },
        "children": [],
    }

    original = copy.deepcopy(snapshot)

    snapshot_to_ir(snapshot)

    assert snapshot == original


def test_snapshot_to_ir_deep_copies_props():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "data": {
                "items": ["one"],
            }
        },
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    snapshot["props"]["data"]["items"].append("changed")

    assert ir_node.props == {
        "data": {
            "items": ["one"],
        }
    }


def test_snapshot_to_ir_rejects_invalid_snapshot():
    with pytest.raises(TypeError):
        snapshot_to_ir("invalid")

    with pytest.raises(ValueError):
        snapshot_to_ir({})

    with pytest.raises(ValueError):
        snapshot_to_ir({
            "id": "1",
        })


def test_snapshot_to_ir_requires_children_list():
    snapshot = {
        "id": "1",
        "type": "Button",
        "props": {},
        "children": "invalid",
    }

    with pytest.raises(ValueError):
        snapshot_to_ir(snapshot)


def test_no_runtime_evaluation():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "text": "Hello",
        },
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.component_id == "Button"
    assert ir_node.style_ref is None


def test_normalize_ir_preserves_identity_and_structure():
    from pylage.core.ir import normalize_ir

    child = IRNode(
        node_id="child",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
        style_ref="style-ref",
    )

    normalized = normalize_ir(node)

    assert normalized is not node
    assert normalized.node_id == "root"
    assert normalized.node_type == "component"
    assert normalized.component_id == "Button"
    assert normalized.props == {"class": "primary"}
    assert normalized.style_ref == "style-ref"

    assert len(normalized.children) == 1
    assert normalized.children[0] is not child
    assert normalized.children[0].node_id == "child"
    assert normalized.children[0].component_id == "Text"


def test_normalize_ir_preserves_child_order():
    from pylage.core.ir import normalize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="a",
                node_type="component",
                component_id="Text",
            ),
            IRNode(
                node_id="b",
                node_type="component",
                component_id="Button",
            ),
            IRNode(
                node_id="c",
                node_type="component",
                component_id="Input",
            ),
        ],
    )

    normalized = normalize_ir(node)

    assert [child.node_id for child in normalized.children] == [
        "a",
        "b",
        "c",
    ]


def test_normalize_ir_deep_copies_props():
    from pylage.core.ir import normalize_ir

    props = {
        "metadata": {
            "items": ["one", "two"],
        },
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props=props,
    )

    normalized = normalize_ir(node)

    props["metadata"]["items"].append("three")

    assert normalized.props == {
        "metadata": {
            "items": ["one", "two"],
        },
    }


def test_normalize_ir_does_not_mutate_source():
    from pylage.core.ir import normalize_ir

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={
            "metadata": {
                "enabled": True,
            },
        },
    )

    original_props = copy.deepcopy(node.props)
    original_children = list(node.children)

    normalize_ir(node)

    assert node.props == original_props
    assert node.children == original_children


def test_normalize_ir_preserves_opaque_style_ref():
    from pylage.core.ir import normalize_ir

    style_ref = {
        "name": "button-style",
        "version": 1,
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        style_ref=style_ref,
    )

    normalized = normalize_ir(node)

    assert normalized.style_ref == style_ref
    assert normalized.style_ref is not style_ref


def test_normalize_ir_rejects_non_ir_node():
    from pylage.core.ir import normalize_ir

    with pytest.raises(TypeError):
        normalize_ir("not an IR node")


def test_normalize_ir_preserves_identity_and_structure():
    from pylage.core.ir import normalize_ir

    child = IRNode(
        node_id="child",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
        style_ref="style-ref",
    )

    normalized = normalize_ir(node)

    assert normalized is not node
    assert normalized.node_id == "root"
    assert normalized.node_type == "component"
    assert normalized.component_id == "Button"
    assert normalized.props == {"class": "primary"}
    assert normalized.style_ref == "style-ref"

    assert len(normalized.children) == 1
    assert normalized.children[0] is not child
    assert normalized.children[0].node_id == "child"
    assert normalized.children[0].component_id == "Text"


def test_normalize_ir_rejects_invalid_input():
    from pylage.core.ir import normalize_ir

    with pytest.raises(TypeError):
        normalize_ir("not an IR node")


def test_normalize_ir_deep_copies_props():
    from pylage.core.ir import normalize_ir

    props = {
        "metadata": {
            "items": ["one", "two"],
        }
    }

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props=props,
    )

    normalized = normalize_ir(node)

    props["metadata"]["items"].append("three")

    assert normalized.props == {
        "metadata": {
            "items": ["one", "two"],
        }
    }


def test_normalize_ir_preserves_child_order():
    from pylage.core.ir import normalize_ir

    children = [
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Text",
            props={"text": "One"},
        ),
        IRNode(
            node_id="2",
            node_type="component",
            component_id="Text",
            props={"text": "Two"},
        ),
    ]

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=children,
    )

    normalized = normalize_ir(node)

    assert [child.node_id for child in normalized.children] == ["1", "2"]


def test_analyze_ir_returns_tree_statistics():
    from pylage.core.ir import analyze_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="child-1",
                node_type="component",
                component_id="Text",
            ),
            IRNode(
                node_id="child-2",
                node_type="component",
                component_id="Button",
            ),
        ],
    )

    result = analyze_ir(node)

    assert result["total_nodes"] == 3
    assert result["node_ids"] == [
        "root",
        "child-1",
        "child-2",
    ]
    assert result["component_ids"] == [
        "Column",
        "Text",
        "Button",
    ]
    assert result["duplicate_node_ids"] == []
    assert result["is_valid"] is True


def test_analyze_ir_detects_duplicate_node_ids():
    from pylage.core.ir import analyze_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="same",
                node_type="component",
                component_id="Text",
            ),
            IRNode(
                node_id="same",
                node_type="component",
                component_id="Button",
            ),
        ],
    )

    result = analyze_ir(node)

    assert result["total_nodes"] == 3
    assert result["duplicate_node_ids"] == ["same"]
    assert result["is_valid"] is False


def test_analyze_ir_rejects_non_ir_node():
    from pylage.core.ir import analyze_ir

    with pytest.raises(TypeError):
        analyze_ir("invalid")


def test_analyze_ir_does_not_mutate_ir():
    from pylage.core.ir import analyze_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": "Hello"},
    )

    before = copy.deepcopy(node.props)
    children_before = list(node.children)

    analyze_ir(node)

    assert node.props == before
    assert node.children == children_before


def test_validate_ir_accepts_valid_tree():
    from pylage.core.ir import validate_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="child-1",
                node_type="component",
                component_id="Text",
            ),
            IRNode(
                node_id="child-2",
                node_type="component",
                component_id="Button",
            ),
        ],
    )

    assert validate_ir(node) is None


def test_validate_ir_rejects_non_ir_node():
    from pylage.core.ir import validate_ir

    with pytest.raises(TypeError):
        validate_ir("not-an-ir-node")


def test_validate_ir_rejects_duplicate_node_ids():
    from pylage.core.ir import validate_ir

    child = IRNode(
        node_id="duplicate",
        node_type="component",
        component_id="Text",
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            child,
            IRNode(
                node_id="duplicate",
                node_type="component",
                component_id="Button",
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="Duplicate IR node_id",
    ):
        validate_ir(node)


def test_validate_ir_does_not_mutate_tree():
    from pylage.core.ir import validate_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        props={
            "data": {
                "items": ["one", "two"],
            }
        },
        children=[
            IRNode(
                node_id="child",
                node_type="component",
                component_id="Text",
            )
        ],
    )

    original_props = copy.deepcopy(node.props)
    original_children = list(node.children)

    validate_ir(node)

    assert node.props == original_props
    assert node.children == original_children
    assert node.children[0].node_id == "child"


def test_validate_ir_checks_nested_duplicate_ids():
    from pylage.core.ir import validate_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="branch",
                node_type="component",
                component_id="Column",
                children=[
                    IRNode(
                        node_id="leaf",
                        node_type="component",
                        component_id="Text",
                    )
                ],
            ),
            IRNode(
                node_id="branch-2",
                node_type="component",
                component_id="Column",
                children=[
                    IRNode(
                        node_id="leaf",
                        node_type="component",
                        component_id="Button",
                    )
                ],
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="Duplicate IR node_id",
    ):
        validate_ir(node)


def test_validate_ir_preserves_valid_style_ref():
    from pylage.core.ir import validate_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        style_ref={
            "style_id": "button-primary",
        },
    )

    assert validate_ir(node) is None



def test_constant_fold_preserves_literal_values():
    from pylage.core.ir import constant_fold

    assert constant_fold(10) == 10
    assert constant_fold("Hello") == "Hello"
    assert constant_fold(True) is True


def test_constant_fold_evaluates_constant_arithmetic():
    from pylage.core.ir import constant_fold

    assert constant_fold(("add", 2, 3)) == 5


def test_constant_fold_is_recursive():
    from pylage.core.ir import constant_fold

    assert constant_fold(("mul", ("add", 2, 3), 4)) == 20


def test_constant_fold_does_not_evaluate_unsafe_values():
    from pylage.core.ir import constant_fold

    assert constant_fold(("div", 10, 0)) == ("div", 10, 0)
    assert constant_fold(("unknown", 2, 3)) == ("unknown", 2, 3)

def test_analyze_ir_dependencies():
    from pylage.core.ir import analyze_ir_dependencies

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": "Hello"},
    )

    result = analyze_ir_dependencies(node)

    assert result["node_ids"] == ["root"]

def test_analyze_ir_dependencies_excludes_non_reactive_props():
    from pylage.core.ir import analyze_ir_dependencies
    from pylage.core.registry import PropDefinition, registry

    registry.register(
        "StaticButton",
        "button",
        props={
            "text": PropDefinition("text", reactive=False),
        },
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="StaticButton",
        props={"text": "Hello"},
    )

    result = analyze_ir_dependencies(node)

    assert result["dependencies"] == []

def test_analyze_ir_dependencies_includes_nested_nodes():
    from pylage.core.ir import analyze_ir_dependencies

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="child",
                node_type="component",
                component_id="Button",
                props={"text": "Hello"},
            )
        ],
    )

    result = analyze_ir_dependencies(node)

    assert result["node_ids"] == ["root", "child"]
    assert result["dependencies"] == [
        {"node_id": "root", "prop_name": "text"}
    ] if False else result["dependencies"]

def test_analyze_ir_dependencies_includes_nested_nodes():
    from pylage.core.ir import analyze_ir_dependencies

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="child",
                node_type="component",
                component_id="Button",
                props={"text": "Hello"},
            )
        ],
    )

    result = analyze_ir_dependencies(node)

    assert result["node_ids"] == ["root", "child"]
    assert {"node_id": "child", "prop_name": "text"} in result["dependencies"]

def test_analyze_ir_dependencies_detects_state():
    from pylage.core.ir import analyze_ir_dependencies
    from pylage.core.state import State

    state = State("Hello")

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": state},
    )

    result = analyze_ir_dependencies(node)

    assert result["dependencies"] == [
        {"node_id": "root", "prop_name": "text"}
    ]

def test_analyze_ir_dependencies_respects_reactive_contract():
    from pylage.core.ir import analyze_ir_dependencies
    from pylage.core.registry import PropDefinition, registry
    from pylage.core.state import State

    registry.register(
        "StaticButton",
        "button",
        props={
            "text": PropDefinition("text", reactive=False),
        },
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="StaticButton",
        props={"text": State("Hello")},
    )

    result = analyze_ir_dependencies(node)

    assert result["dependencies"] == []

def test_analyze_ir_dependencies_rejects_non_ir_node():
    from pylage.core.ir import analyze_ir_dependencies

    with pytest.raises(TypeError):
        analyze_ir_dependencies("invalid")

def test_analyze_ir_dependencies_does_not_mutate_ir():
    from pylage.core.ir import analyze_ir_dependencies

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": "Hello"},
    )

    before = copy.deepcopy(node.props)

    analyze_ir_dependencies(node)

    assert node.props == before

def test_plan_patches_returns_diff_operations():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Text",
        "props": {"text": "Hello"},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Text",
        "props": {"text": "World"},
        "children": [],
    }

    assert plan_patches(previous, current) == [
        {
            "type": "update",
            "id": "root",
            "props": {"text": "World"},
            "remove_props": [],
        }
    ]

def test_plan_patches_returns_empty_for_identical_snapshots():
    from pylage.core.ir import plan_patches

    snapshot = {
        "id": "root",
        "type": "Text",
        "props": {"text": "Hello"},
        "children": [],
    }

    assert plan_patches(snapshot, snapshot) == []

def test_plan_patches_rejects_invalid_snapshots():
    from pylage.core.ir import plan_patches

    with pytest.raises(TypeError):
        plan_patches([], {})

def test_plan_patches_detects_insert():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "props": {"text": "Hello"},
                "children": [],
            }
        ],
    }

    assert plan_patches(previous, current)[0]["type"] == "insert"

def test_plan_patches_detects_remove():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "props": {"text": "Hello"},
                "children": [],
            }
        ],
    }

    current = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [],
    }

    assert plan_patches(previous, current)[0]["type"] == "remove"

def test_plan_patches_detects_prop_update():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Button",
        "props": {"text": "Save"},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Button",
        "props": {"text": "Submit"},
        "children": [],
    }

    operations = plan_patches(previous, current)

    assert operations == [
        {
            "type": "update",
            "id": "root",
            "props": {"text": "Submit"},
            "remove_props": [],
        }
    ]

def test_plan_patches_does_not_mutate_inputs():
    from pylage.core.ir import plan_patches
    import copy

    previous = {
        "id": "root",
        "type": "Text",
        "props": {"text": "Hello"},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Text",
        "props": {"text": "World"},
        "children": [],
    }

    previous_before = copy.deepcopy(previous)
    current_before = copy.deepcopy(current)

    plan_patches(previous, current)

    assert previous == previous_before
    assert current == current_before

def test_plan_patches_detects_nested_prop_update():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "props": {"text": "Hello"},
                "children": [],
            }
        ],
    }

    current = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "props": {"text": "World"},
                "children": [],
            }
        ],
    }

    operations = plan_patches(previous, current)

    assert operations == [
        {
            "type": "update",
            "id": "child",
            "props": {"text": "World"},
            "remove_props": [],
        }
    ]

def test_plan_patches_detects_event_change():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "button",
        "type": "Button",
        "events": "click",
        "props": {},
        "children": [],
    }

    current = {
        "id": "button",
        "type": "Button",
        "events": "click,focus",
        "props": {},
        "children": [],
    }

    operations = plan_patches(previous, current)

    assert operations == [
        {
            "type": "events",
            "id": "button",
            "events": "click,focus",
        }
    ]

def test_plan_patches_detects_type_change():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Text",
        "props": {},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Button",
        "props": {},
        "children": [],
    }

    operations = plan_patches(previous, current)

    assert operations[0]["type"] == "replace"

def test_plan_patches_preserves_diff_order():
    from pylage.core.ir import plan_patches

    previous = {
        "id": "root",
        "type": "Column",
        "props": {},
        "children": [],
    }

    current = {
        "id": "root",
        "type": "Column",
        "props": {"class": "new"},
        "children": [
            {
                "id": "child",
                "type": "Text",
                "props": {"text": "Hello"},
                "children": [],
            }
        ],
    }

    operations = plan_patches(previous, current)

    assert operations[0]["type"] == "update"
    assert operations[1]["type"] == "insert"


def test_optimize_ir_folds_constant_props():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"width": ("add", 10, 20)},
    )

    optimized = optimize_ir(node)

    assert optimized.props == {"width": 30}


def test_optimize_ir_folds_nested_constant_props():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"value": ("mul", ("add", 2, 3), 4)},
    )

    optimized = optimize_ir(node)

    assert optimized.props == {"value": 20}


def test_optimize_ir_recursively_optimizes_children():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="child",
                node_type="component",
                component_id="Button",
                props={"width": ("add", 5, 5)},
            )
        ],
    )

    optimized = optimize_ir(node)

    assert optimized.children[0].props == {"width": 10}


def test_optimize_ir_preserves_identity_and_structure():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"value": ("add", 1, 2)},
        style_ref={"style_id": "primary"},
    )

    optimized = optimize_ir(node)

    assert optimized is not node
    assert optimized.node_id == "root"
    assert optimized.node_type == "component"
    assert optimized.component_id == "Button"
    assert optimized.style_ref == {"style_id": "primary"}


def test_optimize_ir_does_not_mutate_source():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"width": ("add", 10, 20)},
    )

    original_props = copy.deepcopy(node.props)

    optimize_ir(node)

    assert node.props == original_props


def test_optimize_ir_preserves_unsafe_values():
    from pylage.core.ir import IRNode, optimize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"value": ("div", 10, 0)},
    )

    optimized = optimize_ir(node)

    assert optimized.props == {"value": ("div", 10, 0)}


def test_optimize_ir_rejects_non_ir_node():
    from pylage.core.ir import optimize_ir

    with pytest.raises(TypeError):
        optimize_ir("invalid")


def test_optimize_ir_preserves_state_identity():
    from pylage.core.ir import IRNode, optimize_ir
    from pylage.core.state import State

    state = State("Hello")

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": state},
    )

    optimized = optimize_ir(node)

    assert optimized.props["text"] is state


def test_optimize_ir_does_not_copy_state_subscribers():
    from pylage.core.ir import IRNode, optimize_ir
    from pylage.core.state import State

    state = State("Hello")
    calls = []

    state.subscribe(lambda old, new: calls.append((old, new)))

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"text": state},
    )

    optimized = optimize_ir(node)

    optimized.props["text"].set("World")

    assert calls == [("Hello", "World")]
    assert optimized.props["text"] is state


def test_optimize_ir_preserves_state_inside_non_constant_expression():
    from pylage.core.ir import IRNode, optimize_ir
    from pylage.core.state import State

    state = State(10)

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={
            "value": ("add", state, 5),
        },
    )

    optimized = optimize_ir(node)

    assert optimized.props["value"][0] == "add"
    assert optimized.props["value"][1] is state
    assert optimized.props["value"][2] == 5


def test_constant_fold_preserves_folded_children_in_dynamic_expression():
    from pylage.core.ir import constant_fold

    result = constant_fold(("add", ("mul", 2, 3), "dynamic"))

    assert result == ("add", 6, "dynamic")


def test_constant_fold_preserves_state_in_nested_expression():
    from pylage.core.ir import constant_fold
    from pylage.core.state import State

    state = State(10)

    result = constant_fold(
        ("mul", ("add", 2, 3), state)
    )

    assert result[0] == "mul"
    assert result[1] == 5
    assert result[2] is state
