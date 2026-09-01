from pylage.core.binding import StateBinding
from pylage.core.component import Component
from pylage.core.state import State


def test_same_value_state_update_does_not_broadcast():
    state = State("Dollar")

    component = Component(
        type="Input",
        props={"value": state},
    )

    updates = []

    binding = StateBinding(
        component,
        lambda component, props:
            updates.append((component, props)),
    )

    state.set("Racit")
    state.set("Racit")

    assert updates == [
        (component, {"value": "Racit"}),
    ]

    binding.stop()


def test_state_binding_stops_feedback_after_unbind():
    state = State("Dollar")

    component = Component(
        type="Input",
        props={"value": state},
    )

    updates = []

    binding = StateBinding(
        component,
        lambda component, props:
            updates.append(props),
    )

    state.set("Racit")

    binding.stop()

    state.set("Again")

    assert updates == [
        {"value": "Racit"},
    ]
