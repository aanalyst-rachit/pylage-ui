import pylage as ps
from pylage.core.binding import StateBinding
from pylage.core.graph import DependencyGraph


def test_state_binding_builds_dependency_graph():
    state = ps.State(0)
    heading = ps.Heading(text=state)
    app = ps.Column(heading)

    graph = DependencyGraph()

    StateBinding(
        app,
        lambda component, props: None,
        graph=graph,
    )

    assert (heading, "text") in graph.get_dependents(state)
