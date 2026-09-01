from __future__ import annotations

from typing import Any, Callable

from pylage.core.component import Component
from pylage.core.registry import registry
from pylage.core.state import State
from pylage.core.graph import DependencyGraph
from pylage.core.dirty import DirtyNodes
from pylage.core.scheduler import Scheduler


UpdateCallback = Callable[[Component, dict[str, Any]], None]


class StateBinding:
    """Binds reactive State values inside a component tree."""

    def __init__(
        self,
        root: Component,
        callback: UpdateCallback,
        graph: DependencyGraph | None = None,
        dirty: DirtyNodes | None = None,
        scheduler: Scheduler | None = None,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "StateBinding expects a Component root."
            )

        if not callable(callback):
            raise TypeError(
                "StateBinding callback must be callable."
            )

        self.root = root
        self.callback = callback
        self.graph = graph
        self.dirty = dirty
        self.scheduler = scheduler
        self._subscriptions: list[Callable[[], None]] = []

        self._bind_tree(root)

    def _is_reactive(
        self,
        component: Component,
        prop_name: str,
    ) -> bool:
        """Return whether a component prop participates in reactivity."""

        definition = registry.get(component.type)

        if definition is None or definition.props is None:
            # Preserve backward compatibility for unknown components
            # and props that have no registry contract.
            return True

        prop_definition = definition.props.get(prop_name)

        if prop_definition is None:
            # Preserve existing behavior for unknown props.
            return True

        return prop_definition.reactive

    def _bind_tree(self, node: Any) -> None:
        if not isinstance(node, Component):
            return

        for prop_name, value in node.props.items():
            if not isinstance(value, State):
                continue

            if not self._is_reactive(node, prop_name):
                continue

            unsubscribe = value.subscribe(
                lambda old, new,
                component=node,
                name=prop_name: self._changed(
                    component,
                    name,
                    new,
                )
            )

            self._subscriptions.append(unsubscribe)

            if self.graph is not None:
                self.graph.add_dependency(
                    value,
                    node,
                    prop_name,
                )

        for child in node.children:
            self._bind_tree(child)

    def _changed(
        self,
        component: Component,
        prop_name: str,
        value: Any,
    ) -> None:
        # Scheduler mode only marks the component dirty.
        # The scheduler is flushed explicitly at the batching boundary.
        if self.scheduler is not None:
            if self.dirty is not None:
                self.dirty.mark(component)

            self.scheduler.request()
            return

        # Preserve the existing immediate callback contract when
        # no scheduler is configured.
        self.callback(
            component,
            {
                prop_name: value,
            },
        )

        if self.dirty is not None:
            self.dirty.mark(component)

    def stop(self) -> None:
        """Remove all State subscriptions."""

        for unsubscribe in self._subscriptions:
            unsubscribe()

        self._subscriptions.clear()
