from __future__ import annotations

from typing import Any

from pylage.core.component import Component


class EventDispatcher:
    """Dispatches events from a PyLage component tree."""

    def __init__(self, root: Component) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "EventDispatcher expects a Component root."
            )

        self.root = root
        self._components: dict[str, Component] = {}
        self._index_tree(root)

    def _index_tree(self, node: Any) -> None:
        if not isinstance(node, Component):
            return

        self._components[node.id] = node

        for child in node.children:
            self._index_tree(child)

    def dispatch(
        self,
        component_id: str,
        event: str,
        payload: Any = None,
    ) -> Any:
        component = self._components.get(component_id)

        if component is None:
            raise KeyError(
                f"Unknown component id: {component_id}"
            )

        handler = component.events.get(event)

        if handler is None:
            raise KeyError(
                f"Component {component_id!r} "
                f"has no handler for event {event!r}"
            )

        if payload is None:
            return handler()

        return handler(payload)

    def has_component(self, component_id: str) -> bool:
        return component_id in self._components

    def has_event(
        self,
        component_id: str,
        event: str,
    ) -> bool:
        component = self._components.get(component_id)

        if component is None:
            return False

        return event in component.events
