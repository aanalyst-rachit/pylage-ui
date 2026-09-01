from pylage.core.state import State


def test_same_value_does_not_notify():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(0)

    assert changes == []


def test_different_value_notifies_once():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)

    assert changes == [(0, 1)]


def test_multiple_changes_preserve_order():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)
    state.set(2)
    state.set(3)

    assert changes == [
        (0, 1),
        (1, 2),
        (2, 3),
    ]


def test_multiple_subscribers_all_receive_update():
    state = State("initial")

    first = []
    second = []

    state.subscribe(
        lambda old, new: first.append((old, new))
    )

    state.subscribe(
        lambda old, new: second.append((old, new))
    )

    state.set("updated")

    assert first == [("initial", "updated")]
    assert second == [("initial", "updated")]


def test_unsubscribe_stops_future_notifications():
    state = State(0)
    changes = []

    unsubscribe = state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)
    unsubscribe()
    state.set(2)

    assert changes == [(0, 1)]


def test_unsubscribe_is_idempotent():
    state = State(0)
    changes = []

    unsubscribe = state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    unsubscribe()
    unsubscribe()

    state.set(1)

    assert changes == []


def test_subscriber_can_unsubscribe_during_notification():
    state = State(0)
    changes = []

    unsubscribe = None

    def listener(old, new):
        changes.append((old, new))
        unsubscribe()

    unsubscribe = state.subscribe(listener)

    state.set(1)
    state.set(2)

    assert changes == [(0, 1)]


def test_subscriber_iteration_is_stable():
    state = State(0)
    changes = []

    def first(old, new):
        changes.append(("first", old, new))

        state.subscribe(
            lambda old, new: changes.append(
                ("late", old, new)
            )
        )

    state.subscribe(first)

    state.set(1)

    assert changes == [
        ("first", 0, 1),
    ]

    state.set(2)

    assert changes == [
        ("first", 0, 1),
        ("first", 1, 2),
        ("late", 1, 2),
    ]
