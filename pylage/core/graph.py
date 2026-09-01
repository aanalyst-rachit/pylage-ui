from __future__ import annotations

from typing import Set, Tuple
from pylage.core.component import Component
from pylage.core.state import State


class DependencyGraph:
    """Tracks directed dependencies between State containers and Component properties."""

    def __init__(self) -> None:
        self._state_to_components: dict[State, set[tuple[Component, str]]] = {}

    def add_dependency(self, state: State, component: Component, prop_name: str) -> None:
        """Register a dependency between a State object and a Component prop."""
        if state not in self._state_to_components:
            self._state_to_components[state] = set()
        self._state_to_components[state].add((component, prop_name))

    def remove_dependency(self, state: State, component: Component, prop_name: str) -> None:
        """Remove a specific dependency edge."""
        if state in self._state_to_components:
            self._state_to_components[state].discard((component, prop_name))
            if not self._state_to_components[state]:
                del self._state_to_components[state]

    def get_dependents(self, state: State) -> set[tuple[Component, str]]:
        """Return all (Component, prop_name) tuples dependent on the given State."""
        return self._state_to_components.get(state, set())

    def clear(self) -> None:
        """Clear all registered dependencies."""
        self._state_to_components.clear()
