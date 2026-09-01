from pylage.runtime.client import get_client_runtime


print("=== PYLAGE CLIENT RUNTIME TEST ===")

runtime = get_client_runtime()

print("Runtime bytes:", len(runtime.encode("utf-8")))

assert isinstance(runtime, str)
assert len(runtime) > 0

assert "data-pylage-id" in runtime
assert "data-pylage-events" in runtime
assert "sendEvent" in runtime
assert "type: \"event\"" in runtime
assert "document.addEventListener" in runtime

print("Runtime present: PASS")
print("Event detection logic: PASS")
print("Event message generation: PASS")

print("=== CLIENT RUNTIME PASS ===")

def test_runtime_contains_tree_add_patch_handler():
    runtime = get_client_runtime()

    assert "tree_add" in runtime
    assert "parent_id" in runtime
    assert "components" in runtime

def test_runtime_contains_nested_tree_add_support():
    runtime = get_client_runtime()

    assert "item.children" in runtime
    assert "appendChild" in runtime

def test_runtime_contains_tree_remove_patch_handler():
    runtime = get_client_runtime()

    assert "tree_remove" in runtime
    assert "component_ids" in runtime
    assert "remove()" in runtime

def test_runtime_tree_remove_handles_multiple_component_ids():
    runtime = get_client_runtime()

    assert "message.component_ids.forEach" in runtime
    assert "CSS.escape(componentId)" in runtime
    assert "component.remove()" in runtime

def test_runtime_tree_remove_supports_multiple_component_ids():
    runtime = get_client_runtime()

    assert "message.component_ids.forEach" in runtime
    assert "component.remove()" in runtime


def test_runtime_contains_tree_move_patch_handler():
    runtime = get_client_runtime()

    assert "tree_move" in runtime
    assert "old_parent_id" in runtime
    assert "new_parent_id" in runtime
    assert "component_id" in runtime


def test_runtime_tree_move_uses_append_child():
    runtime = get_client_runtime()

    assert "newParent.appendChild(component)" in runtime


def test_runtime_tree_move_preserves_existing_subtree():
    runtime = get_client_runtime()

    assert "appendChild(component)" in runtime
    assert "component_id" in runtime
    assert "new_parent_id" in runtime


def test_runtime_tree_add_supports_indexed_insertion():
    runtime = get_client_runtime()

    assert "message.index" in runtime
    assert "insertBefore" in runtime


def test_runtime_tree_add_multiple_components_uses_index():
    runtime = get_client_runtime()

    assert "message.components.forEach" in runtime
    assert "message.index" in runtime
    assert "parent.children[message.index]" in runtime
    assert "insertBefore" in runtime


def test_runtime_contains_tree_replace_patch_handler():
    runtime = get_client_runtime()

    assert "tree_replace" in runtime
    assert "message.old_component_id" in runtime
    assert "message.new_component" in runtime


def test_runtime_contains_tree_clear_patch_handler():
    runtime = get_client_runtime()

    assert "tree_clear" in runtime
    assert "message.parent_id" in runtime
    assert "message.component_ids" in runtime


def test_runtime_contains_tree_set_children_patch_handler():
    runtime = get_client_runtime()

    assert "tree_set_children" in runtime
    assert "message.parent_id" in runtime
    assert "message.children" in runtime
