from pylage.runtime.client import CLIENT_RUNTIME


def test_tree_clear_client_removes_listed_children():
    runtime = CLIENT_RUNTIME

    assert "message.component_ids" in runtime
    assert "parent.removeChild(child)" in runtime
    assert "Array.from(parent.children)" in runtime


def test_tree_clear_client_preserves_unlisted_children():
    runtime = CLIENT_RUNTIME

    assert "componentIds.has(componentId)" in runtime
    assert "if (componentIds.has(componentId))" in runtime


def test_tree_clear_client_keeps_parent_node():
    runtime = CLIENT_RUNTIME

    assert "const parent = document.querySelector(" in runtime
    assert "parent.removeChild(child)" in runtime


def test_tree_clear_client_removes_nested_subtree_with_direct_child():
    runtime = CLIENT_RUNTIME

    assert "Array.from(parent.children)" in runtime
    assert "const componentId = child.getAttribute(" in runtime
    assert "componentIds.has(componentId)" in runtime
    assert "parent.removeChild(child)" in runtime
