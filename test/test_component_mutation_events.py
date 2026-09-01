from pylage.core.component import Component


def test_add_notifies_tree_mutation_listener():
    parent = Component(type="Column")
    child = Component(type="Heading")

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.add(child)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "add"
    assert event["parent"] is parent
    assert event["children"] == [child]


def test_unsubscribe_stops_mutation_notifications():
    parent = Component(type="Column")
    child = Component(type="Heading")

    mutations = []

    unsubscribe = parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    unsubscribe()

    parent.add(child)

    assert mutations == []


def test_mutation_subscription_is_idempotently_removable():
    parent = Component(type="Column")

    mutations = []

    unsubscribe = parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    unsubscribe()
    unsubscribe()

    parent.add(Component(type="Heading"))

    assert mutations == []

def test_move_to_emits_single_move_mutation_event():
    parent_a = Component(type="Column")
    parent_b = Component(type="Column")
    child = Component(type="Button")

    parent_a.add(child)

    mutations = []

    parent_a.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent_b.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    child.move_to(parent_b)

    move_events = [
        event
        for event in mutations
        if event.get("type") == "move"
    ]

    assert len(move_events) == 1

    event = move_events[0]

    assert event["component"] is child
    assert event["old_parent"] is parent_a
    assert event["new_parent"] is parent_b


def test_insert_emits_add_mutation_with_index():
    parent = Component(type="Column")
    first = Component(type="Button")
    second = Component(type="Button")

    parent.add(first)

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.insert(1, second)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "add"
    assert event["parent"] is parent
    assert event["children"] == [second]
    assert event["index"] == 1


def test_insert_multiple_children_emits_single_mutation_event():
    parent = Component(type="Column")
    first = Component(type="Button")

    parent.add(first)

    child_a = Component(type="Button")
    child_b = Component(type="Button")

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.insert(1, child_a, child_b)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "add"
    assert event["parent"] is parent
    assert event["children"] == [child_a, child_b]
    assert event["index"] == 1


def test_replace_emits_replace_mutation_event():
    parent = Component(type="Column")
    old_child = Component(type="Button")
    new_child = Component(type="Text")

    parent.add(old_child)

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.replace(old_child, new_child)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "replace"
    assert event["parent"] is parent
    assert event["old_child"] is old_child
    assert event["new_child"] is new_child
    assert event["index"] == 0


def test_clear_emits_single_clear_mutation_event():
    parent = Component(type="Column")
    first = Component(type="Button")
    second = Component(type="Text")
    third = Component(type="Button")

    parent.add(first, second, third)

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.clear()

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "clear"
    assert event["parent"] is parent
    assert event["children"] == [first, second, third]


def test_set_children_emits_single_set_children_mutation_event():
    parent = Component(type="Column")

    old_first = Component(type="Button")
    old_second = Component(type="Text")

    new_first = Component(type="Text")
    new_second = Component(type="Button")

    parent.add(old_first, old_second)

    mutations = []

    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.set_children(new_first, new_second)

    assert len(mutations) == 1

    event = mutations[0]

    assert event["type"] == "set_children"
    assert event["parent"] is parent
    assert event["old_children"] == [old_first, old_second]
    assert event["children"] == [new_first, new_second]
