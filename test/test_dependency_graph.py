import pytest
from pylage.core.component import Component
from pylage.core.state import State
from pylage.core.graph import DependencyGraph


def test_add_and_get_dependents():
    graph = DependencyGraph()
    state = State("initial")
    comp = Component("div")

    graph.add_dependency(state, comp, "text")
    dependents = graph.get_dependents(state)

    assert len(dependents) == 1
    assert (comp, "text") in dependents


def test_multiple_dependents_for_same_state():
    graph = DependencyGraph()
    state = State(10)
    comp1 = Component("p")
    comp2 = Component("span")

    graph.add_dependency(state, comp1, "count")
    graph.add_dependency(state, comp2, "value")

    dependents = graph.get_dependents(state)
    assert len(dependents) == 2
    assert (comp1, "count") in dependents
    assert (comp2, "value") in dependents


def test_remove_dependency():
    graph = DependencyGraph()
    state = State("active")
    comp = Component("button")

    graph.add_dependency(state, comp, "disabled")
    graph.remove_dependency(state, comp, "disabled")

    assert len(graph.get_dependents(state)) == 0


def test_graph_clear():
    graph = DependencyGraph()
    state1 = State("a")
    state2 = State("b")
    comp = Component("div")

    graph.add_dependency(state1, comp, "id")
    graph.add_dependency(state2, comp, "class")

    graph.clear()
    assert len(graph.get_dependents(state1)) == 0
    assert len(graph.get_dependents(state2)) == 0
