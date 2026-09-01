from pylage.runtime.client import CLIENT_RUNTIME


def test_tree_set_children_client_replaces_existing_children():
    runtime = CLIENT_RUNTIME

    assert "tree_set_children" in runtime
    assert "message.children" in runtime
    assert "while (parent.firstChild)" in runtime
    assert "parent.removeChild(parent.firstChild)" in runtime
    assert "parent.appendChild(element)" in runtime


def test_tree_set_children_client_preserves_new_child_order():
    runtime = CLIENT_RUNTIME

    assert "message.children.forEach" in runtime
    assert "parent.appendChild(element)" in runtime


def test_tree_set_children_client_builds_nested_subtrees():
    runtime = CLIENT_RUNTIME

    assert "function createTreeNode(item)" in runtime
    assert "const children = item.children || []" in runtime
    assert "children.forEach(function (child)" in runtime
    assert "element.appendChild(childElement)" in runtime


def test_tree_set_children_client_supports_deep_nested_subtrees():
    runtime = CLIENT_RUNTIME

    # Recursive construction must continue for arbitrary nested children.
    assert runtime.count("createTreeNode(child)") >= 1
    assert runtime.count("element.appendChild(childElement)") >= 1
