from pylage.core.binding import StateBinding
from pylage.core.component import Component
from pylage.core.registry import ComponentRegistry, PropDefinition
from pylage.core.state import State
import pylage.core.binding as binding_module


def make_registry():
    registry = ComponentRegistry()

    registry.register(
        "TestComponent",
        "div",
        props={
            "reactive": PropDefinition(
                "reactive",
                reactive=True,
            ),
            "static": PropDefinition(
                "static",
                reactive=False,
            ),
        },
    )

    return registry


def test_reactive_and_non_reactive_props():
    registry = make_registry()

    original_registry = binding_module.registry
    binding_module.registry = registry

    try:
        reactive = State("one")
        static = State("one")

        component = Component(
            type="TestComponent",
            props={
                "reactive": reactive,
                "static": static,
            },
        )

        updates = []

        binding = StateBinding(
            component,
            lambda component, props:
                updates.append((component, props)),
        )

        reactive.set("two")
        static.set("two")

        assert updates == [
            (component, {"reactive": "two"})
        ]

        binding.stop()

    finally:
        binding_module.registry = original_registry


def test_stop_removes_all_subscriptions():
    registry = make_registry()

    original_registry = binding_module.registry
    binding_module.registry = registry

    try:
        first = State(1)
        second = State(2)

        component = Component(
            type="TestComponent",
            props={
                "reactive": first,
                "other": second,
            },
        )

        updates = []

        binding = StateBinding(
            component,
            lambda component, props:
                updates.append((component, props)),
        )

        first.set(10)
        second.set(20)

        assert len(updates) == 2

        binding.stop()

        first.set(100)
        second.set(200)

        assert len(updates) == 2

    finally:
        binding_module.registry = original_registry


def test_stop_is_idempotent():
    component = Component(
        type="Unknown",
        props={
            "value": State(0),
        },
    )

    updates = []

    binding = StateBinding(
        component,
        lambda component, props:
            updates.append((component, props)),
    )

    binding.stop()
    binding.stop()

    component.props["value"].set(1)

    assert updates == []


def test_nested_components_are_bound():
    parent_state = State("parent")
    child_state = State("child")

    child = Component(
        type="Child",
        props={
            "value": child_state,
        },
    )

    root = Component(
        type="Root",
        props={
            "value": parent_state,
        },
        children=[child],
    )

    updates = []

    binding = StateBinding(
        root,
        lambda component, props:
            updates.append((component, props)),
    )

    parent_state.set("parent-updated")
    child_state.set("child-updated")

    assert updates == [
        (root, {"value": "parent-updated"}),
        (child, {"value": "child-updated"}),
    ]

    binding.stop()
