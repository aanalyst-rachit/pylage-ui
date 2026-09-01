from __future__ import annotations

from pylage.core.component import Component
from pylage.core.graph import DependencyGraph
from pylage.core.state import State


class DirtyNodes:
    """Tracks components invalidated by reactive state changes."""

    def __init__(self) -> None:
        self._nodes: set[Component] = set()
        self._ordered_nodes: list[Component] = []

    def mark(self, component: Component) -> None:
        if component in self._nodes:
            return

        self._nodes.add(component)
        self._ordered_nodes.append(component)

    def nodes(self) -> list[Component]:
        """Return dirty components in deterministic insertion order."""
        return list(self._ordered_nodes)

    def mark_from_state(
        self,
        state: State,
        graph: DependencyGraph,
    ) -> None:
        for component, _prop_name in graph.get_dependents(state):
            self.mark(component)

    def contains(self, component: Component) -> bool:
        return component in self._nodes

    def clear(self) -> None:
        self._nodes.clear()
        self._ordered_nodes.clear()

    def __len__(self) -> int:
        return len(self._nodes)
