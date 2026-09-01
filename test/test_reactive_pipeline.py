import pylage as ps

from pylage.core.binding import StateBinding
from pylage.core.dirty import DirtyNodes
from pylage.core.graph import DependencyGraph
from pylage.core.scheduler import Scheduler


def test_state_change_flows_through_reactive_pipeline():
    state = ps.State(0)
    heading = ps.Heading(text=state)
    app = ps.Column(heading)

    graph = DependencyGraph()
    dirty = DirtyNodes()
    updates = []

    StateBinding(
        app,
        lambda component, props: updates.append(
            (component, props)
        ),
        graph=graph,
    )

    state.set(1)

    dirty.mark_from_state(state, graph)

    scheduler = Scheduler(
        dirty,
        lambda component: updates.append(
            (component, {"scheduled": True})
        ),
    )

    scheduler.flush()

    assert heading in [item[0] for item in updates]
    assert len(dirty) == 0
