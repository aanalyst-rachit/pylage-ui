from pylage.runtime.client import CLIENT_RUNTIME


def test_tree_replace_client_replaces_old_node_at_same_position():
    runtime = CLIENT_RUNTIME

    assert "oldComponent.replaceWith(newComponent)" in runtime
    assert "message.new_component" in runtime
    assert "CSS.escape(message.old_component_id)" in runtime


def test_tree_replace_client_creates_replacement_tree_node():
    runtime = CLIENT_RUNTIME

    assert "document.createElement" in runtime
    assert "item.tag || \"div\"" in runtime
    assert "item.props" in runtime
    assert "item.children" in runtime


def test_tree_replace_client_supports_nested_replacement_tree():
    runtime = CLIENT_RUNTIME

    assert "const children = item.children || [];" in runtime
    assert "children.forEach" in runtime
    assert "createTreeNode(child)" in runtime
    assert "element.appendChild(childElement)" in runtime


def test_tree_replace_client_replaces_nested_subtree():
    runtime = CLIENT_RUNTIME

    assert "oldComponent.replaceWith(newComponent)" in runtime
    assert "const children = item.children || [];" in runtime
    assert "children.forEach(function (child)" in runtime
    assert "const childElement = createTreeNode(child);" in runtime
    assert "element.appendChild(childElement);" in runtime
