from time import perf_counter

from pylage.core.component import Component
from pylage.core.dirty import DirtyNodes
from pylage.core.scheduler import Scheduler
from pylage.core.state import State
from pylage.core.binding import StateBinding


def _build_reactive_pipeline():
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


def _batched_updates(count: int):
    state, component, scheduler, processed = _build_reactive_pipeline()

    start = perf_counter()

    for value in range(1, count + 1):
        state.set(value)

    scheduler.flush()

    elapsed = perf_counter() - start

    return {
        "elapsed": elapsed,
        "updates": len(processed),
        "final_value": state.value,
    }


def _unbatched_updates(count: int):
    state, component, scheduler, processed = _build_reactive_pipeline()

    start = perf_counter()

    for value in range(1, count + 1):
        state.set(value)
        scheduler.flush()

    elapsed = perf_counter() - start

    return {
        "elapsed": elapsed,
        "updates": len(processed),
        "final_value": state.value,
    }


def test_batching_reduces_processing_cycles():
    batched = _batched_updates(100)
    unbatched = _unbatched_updates(100)

    assert batched["updates"] == 1
    assert unbatched["updates"] == 100

    assert batched["final_value"] == 100
    assert unbatched["final_value"] == 100


def test_batching_benchmark_report():
    count = 1000

    batched = _batched_updates(count)
    unbatched = _unbatched_updates(count)

    print()
    print("===== PHASE 2E BATCHING BENCHMARK =====")
    print(f"State changes       : {count}")
    print()
    print("BATCHED")
    print(f"  processing cycles : {batched['updates']}")
    print(f"  final value       : {batched['final_value']}")
    print(f"  elapsed           : {batched['elapsed']:.9f}s")
    print()
    print("UNBATCHED")
    print(f"  processing cycles : {unbatched['updates']}")
    print(f"  final value       : {unbatched['final_value']}")
    print(f"  elapsed           : {unbatched['elapsed']:.9f}s")
    print()
    print(
        "processing reduction: "
        f"{unbatched['updates'] / batched['updates']:.1f}x"
    )

    assert batched["updates"] == 1
    assert unbatched["updates"] == count
    assert batched["final_value"] == count
    assert unbatched["final_value"] == count
