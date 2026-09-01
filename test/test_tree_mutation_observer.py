from pylage.core.component import Component
from pylage.core.tree import TreeMutationObserver


def test_observer_receives_nested_add_mutations():
    child = Component(type="Column")
    root = Component(
        type="Column",
        children=[child],
    )

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    grandchild = Component(type="Button")
    child.add(grandchild)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "add"
    assert mutations[0]["parent"] is child
    assert mutations[0]["children"] == [grandchild]

    observer.stop()


def test_observer_can_be_stopped():
    root = Component(type="Column")
    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.add(Component(type="Heading"))

    assert len(mutations) == 1

    observer.stop()

    root.add(Component(type="Button"))

    assert len(mutations) == 1


def test_observer_stop_is_idempotent():
    root = Component(type="Column")

    observer = TreeMutationObserver(
        root,
        lambda event: None,
    )

    observer.stop()
    observer.stop()


def test_observer_tracks_components_added_after_observer_creation():
    root = Component(type="Column")

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    child = Component(type="Column")
    root.add(child)

    # The add to root is observed.
    assert len(mutations) == 1

    button = Component(type="Button")
    child.add(button)

    # The newly-added child is now also observed.
    assert len(mutations) == 2
    assert mutations[1]["parent"] is child
    assert mutations[1]["children"] == [button]

    observer.stop()


def test_observer_does_not_bind_same_component_twice():
    root = Component(type="Column")
    child = Component(type="Column")

    root.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    # Move the already-observed component inside the same tree.
    child.move_to(root)

    button = Component(type="Button")
    child.add(button)

    # The child's mutation must be delivered exactly once.
    assert len(mutations) == 2
    assert mutations[0]["type"] == "move"
    assert mutations[1]["type"] == "add"

    observer.stop()


def test_observer_does_not_duplicate_bind_on_set_children():
    root = Component(type="Column")
    child = Component(type="Column")

    root.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.set_children(child)

    button = Component(type="Button")
    child.add(button)

    # set_children itself + child's add.
    # Child mutation must be delivered exactly once.
    assert len(mutations) == 2
    assert mutations[0]["type"] == "set_children"
    assert mutations[1]["type"] == "add"

    observer.stop()


def test_observer_tracks_component_added_by_replace():
    root = Component(type="Column")
    old_child = Component(type="Button")
    new_child = Component(type="Column")

    root.add(old_child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.replace(old_child, new_child)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "replace"

    button = Component(type="Button")
    new_child.add(button)

    # The replacement component must now be observed.
    assert len(mutations) == 2
    assert mutations[1]["type"] == "add"
    assert mutations[1]["parent"] is new_child

    observer.stop()


def test_observer_stops_tracking_removed_component():
    root = Component(type="Column")
    child = Component(type="Column")

    root.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.remove(child)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "remove"

    child.add(Component(type="Button"))

    # Removed subtree must no longer notify the tree observer.
    assert len(mutations) == 1

    observer.stop()


def test_observer_tracks_component_after_move():
    root = Component(type="Column")
    parent_a = Component(type="Column")
    parent_b = Component(type="Column")
    child = Component(type="Column")

    root.add(parent_a, parent_b)
    parent_a.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    child.move_to(parent_b)

    button = Component(type="Button")
    child.add(button)

    move_events = [
        event
        for event in mutations
        if event.get("type") == "move"
    ]

    assert len(move_events) == 1

    # The moved subtree must remain observed.
    assert len(mutations) == 2
    assert mutations[1]["type"] == "add"
    assert mutations[1]["parent"] is child
    assert mutations[1]["children"] == [button]

    observer.stop()


def test_observer_move_event_contains_correct_parent_relationship():
    root = Component(type="Column")
    old_parent = Component(type="Column")
    new_parent = Component(type="Column")
    child = Component(type="Button")

    root.add(old_parent, new_parent)
    old_parent.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    child.move_to(new_parent)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "move"
    assert event["component"] is child
    assert event["old_parent"] is old_parent
    assert event["new_parent"] is new_parent

    assert child._parent is new_parent
    assert child not in old_parent.children
    assert child in new_parent.children

    observer.stop()


def test_observer_stop_then_new_tree_mutation_does_not_reactivate():
    root = Component(type="Column")
    child = Component(type="Column")

    root.add(child)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    observer.stop()

    root.add(Component(type="Button"))
    child.add(Component(type="Button"))

    assert mutations == []
    assert observer._subscriptions == []
    assert observer._component_unsubscribers == {}
    assert observer._bound_components == set()


def test_observer_stops_tracking_subtree_removed_by_clear():
    root = Component(type="Column")
    child = Component(type="Column")
    grandchild = Component(type="Column")

    root.add(child)
    child.add(grandchild)

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.clear()

    assert len(mutations) == 1
    assert mutations[0]["type"] == "clear"

    grandchild.add(Component(type="Button"))

    assert len(mutations) == 1

    observer.stop()
