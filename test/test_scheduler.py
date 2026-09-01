from pylage.core.component import Component
from pylage.core.dirty import DirtyNodes
from pylage.core.scheduler import Scheduler
from pylage.core.state import State
from pylage.core.binding import StateBinding


def test_scheduler_request_coalescing():
    """Multiple scheduler requests are coalesced into one scheduled flush."""
    flush_count = 0

    def fake_schedule_flush():
        nonlocal flush_count
        flush_count += 1

    scheduler = Scheduler(
        DirtyNodes(),
        lambda node: None,
        schedule_flush=fake_schedule_flush,
    )

    scheduler.request()
    scheduler.request()
    scheduler.request()

    assert flush_count == 1

    scheduler.flush()

    scheduler.request()

    assert flush_count == 2


def test_multiple_states_same_component():
    """Multiple State changes affecting one component are processed once."""
    state1 = State(0)
    state2 = State(0)

    component = Component(
        type="Heading",
        props={
            "prop1": state1,
            "prop2": state2,
        },
    )

    dirty = DirtyNodes()
    processed = []

    scheduler = Scheduler(
        dirty,
        lambda node: processed.append(node),
    )

    StateBinding(
        component,
        lambda component, props: None,
        dirty=dirty,
        scheduler=scheduler,
    )

    state1.set(1)
    state2.set(2)

    assert len(dirty) == 1
    assert dirty.contains(component)

    scheduler.flush()

    assert processed == [component]
    assert len(dirty) == 0


def test_final_value():
    """A scheduled component observes the final current State value."""
    state = State(0)

    component = Component(
        type="Heading",
        props={
            "text": state,
        },
    )

    dirty = DirtyNodes()
    observed = []

    scheduler = Scheduler(
        dirty,
        lambda node: observed.append(
            {
                name: value.value
                if isinstance(value, State)
                else value
                for name, value in node.props.items()
            }
        ),
    )

    StateBinding(
        component,
        lambda component, props: None,
        dirty=dirty,
        scheduler=scheduler,
    )

    state.set(1)
    state.set(2)
    state.set(3)

    assert len(dirty) == 1

    scheduler.flush()

    assert observed == [{"text": 3}]
    assert len(dirty) == 0


def test_deterministic_dirty_order():
    """Dirty components are processed in first-mark order."""
    dirty = DirtyNodes()

    component_a = Component(type="A")
    component_b = Component(type="B")
    component_c = Component(type="C")

    dirty.mark(component_a)
    dirty.mark(component_b)
    dirty.mark(component_c)
    dirty.mark(component_a)

    assert dirty.nodes() == [
        component_a,
        component_b,
        component_c,
    ]

    flushed = []

    scheduler = Scheduler(
        dirty,
        lambda node: flushed.append(node),
    )

    scheduler.flush()

    assert flushed == [
        component_a,
        component_b,
        component_c,
    ]


def test_re_entrant_state_change():
    """
    A State change during a flush creates work for the next cycle,
    rather than recursively processing during the current cycle.
    """
    state = State(0)

    component = Component(
        type="Heading",
        props={
            "value": state,
        },
    )

    dirty = DirtyNodes()

    StateBinding(
        component,
        lambda component, props: None,
        dirty=dirty,
    )

    state.set(1)

    assert len(dirty) == 1

    processed = []

    def callback(node):
        processed.append(node)
        state.set(state.value + 1)

    scheduler = Scheduler(
        dirty,
        callback,
    )

    scheduler.flush()

    assert processed == [component]

    # The callback changed the State during the flush.
    # That new work must remain for the next scheduler cycle.
    assert len(dirty) == 1
    assert dirty.contains(component)

    scheduler.flush()

    assert processed == [
        component,
        component,
    ]

    assert len(dirty) == 1


def test_flush_clears_before_callback():
    """The current dirty set is cleared before callbacks execute."""
    dirty = DirtyNodes()
    component = Component(type="Heading")

    dirty.mark(component)

    def callback(node):
        assert len(dirty) == 0

    scheduler = Scheduler(
        dirty,
        callback,
    )

    scheduler.flush()

    assert len(dirty) == 0


def test_scheduler_flush_can_be_scheduled_only_once_per_batch():
    dirty = DirtyNodes()
    component = Component(type="Heading")
    scheduled = []
    processed = []

    scheduler = Scheduler(
        dirty,
        lambda node: processed.append(node),
        schedule_flush=lambda: scheduled.append(True),
    )

    dirty.mark(component)

    scheduler.request()
    scheduler.request()
    scheduler.request()

    assert scheduled == [True]

    scheduler.flush()

    assert processed == [component]

    scheduler.request()

    assert scheduled == [True, True]
