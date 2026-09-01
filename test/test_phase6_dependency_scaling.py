from time import perf_counter

from pylage.core.component import Component
from pylage.core.graph import DependencyGraph
from pylage.core.state import State


SIZES = (10, 100, 1_000, 10_000)


def _build_graph(size: int):
    graph = DependencyGraph()
    state = State(0)

    components = [
        Component(
            type="Heading",
            props={"text": str(index)},
        )
        for index in range(size)
    ]

    for index, component in enumerate(components):
        graph.add_dependency(
            state,
            component,
            f"prop_{index}",
        )

    return graph, state, components


def _measure_get_dependents(graph, state, iterations=100):
    start = perf_counter()

    for _ in range(iterations):
        dependents = graph.get_dependents(state)

    elapsed = perf_counter() - start

    return elapsed, dependents


def test_phase6_dependency_graph_scaling():
    print()
    print("===== PHASE 6 — DEPENDENCY GRAPH SCALING =====")

    for size in SIZES:
        graph, state, components = _build_graph(size)

        elapsed, dependents = _measure_get_dependents(
            graph,
            state,
            iterations=100,
        )

        assert len(dependents) == size

        print()
        print(f"dependencies       : {size}")
        print(f"components         : {len(components)}")
        print(f"get_dependents     : {elapsed:.9f}s")
        print(
            f"per lookup         : "
            f"{elapsed / 100:.9f}s"
        )


def test_phase6_dependency_graph_registration_scaling():
    print()
    print("===== PHASE 6 — DEPENDENCY REGISTRATION =====")

    for size in SIZES:
        graph = DependencyGraph()
        state = State(0)

        components = [
            Component(type="Heading")
            for _ in range(size)
        ]

        start = perf_counter()

        for index, component in enumerate(components):
            graph.add_dependency(
                state,
                component,
                f"prop_{index}",
            )

        elapsed = perf_counter() - start

        assert len(graph.get_dependents(state)) == size

        print()
        print(f"dependencies       : {size}")
        print(f"registration       : {elapsed:.9f}s")
        print(
            f"per registration   : "
            f"{elapsed / size:.9f}s"
        )
