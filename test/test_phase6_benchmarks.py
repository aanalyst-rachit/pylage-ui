from time import perf_counter

from pylage.core.component import Component
from pylage.core.dirty import DirtyNodes
from pylage.core.scheduler import Scheduler
from pylage.core.state import State
from pylage.core.binding import StateBinding
from pylage.core.snapshot import component_to_snapshot
from pylage.core.diff import diff
from pylage.core.patch import operations_to_messages


def _build_pipeline():
    state = State(0)

    component = Component(
        type="Heading",
        props={"text": state},
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

    return state, component, scheduler, processed


def _measure(fn, iterations=1000):
    start = perf_counter()

    for _ in range(iterations):
        fn()

    elapsed = perf_counter() - start

    return {
        "total": elapsed,
        "per_operation": elapsed / iterations,
    }


def test_phase6_state_update_latency():
    state, _, _, _ = _build_pipeline()

    result = _measure(
        lambda: state.set(state.value + 1),
        iterations=1000,
    )

    assert state.value == 1000
    assert result["total"] >= 0
    assert result["per_operation"] >= 0

    print()
    print("===== PHASE 6 — STATE UPDATE LATENCY =====")
    print(f"iterations        : 1000")
    print(f"total             : {result['total']:.9f}s")
    print(f"per update        : {result['per_operation']:.9f}s")


def test_phase6_scheduler_latency():
    state, _, scheduler, processed = _build_pipeline()

    for value in range(1000):
        state.set(value)

    result = _measure(
        scheduler.flush,
        iterations=1,
    )

    assert state.value == 999
    assert len(processed) == 1

    print()
    print("===== PHASE 6 — SCHEDULER FLUSH =====")
    print(f"dirty updates     : 1000")
    print(f"processing cycles : {len(processed)}")
    print(f"elapsed           : {result['total']:.9f}s")


def test_phase6_diff_latency():
    previous = {
        "id": "root",
        "type": "Heading",
        "props": {"text": "before"},
        "children": [],
        "events": "",
    }

    current = {
        "id": "root",
        "type": "Heading",
        "props": {"text": "after"},
        "children": [],
        "events": "",
    }

    result = _measure(
        lambda: diff(previous, current),
        iterations=1000,
    )

    operations = diff(previous, current)

    assert len(operations) == 1
    assert operations[0]["type"] == "update"

    print()
    print("===== PHASE 6 — DIFF LATENCY =====")
    print(f"iterations        : 1000")
    print(f"operations        : {len(operations)}")
    print(f"total             : {result['total']:.9f}s")
    print(f"per diff          : {result['per_operation']:.9f}s")


def test_phase6_patch_latency():
    operations = [
        {
            "type": "update",
            "id": "root",
            "props": {"text": "after"},
            "remove_props": [],
        }
    ]

    result = _measure(
        lambda: operations_to_messages(operations),
        iterations=1000,
    )

    messages = operations_to_messages(operations)

    assert len(messages) == 1

    print()
    print("===== PHASE 6 — PATCH LATENCY =====")
    print(f"iterations        : 1000")
    print(f"messages          : {len(messages)}")
    print(f"total             : {result['total']:.9f}s")
    print(f"per conversion    : {result['per_operation']:.9f}s")
