from __future__ import annotations

from typing import Any, Callable


Subscriber = Callable[[Any, Any], None]


class State:
    """Reactive state value used by the pylage runtime."""

    def __init__(self, value: Any = None):
        self._value = value
        self._subscribers: list[Subscriber] = []

    @property
    def value(self) -> Any:
        return self._value

    def set(self, value: Any) -> None:
        old_value = self._value

        if old_value == value:
            return

        self._value = value

        for subscriber in tuple(self._subscribers):
            subscriber(old_value, value)

    def subscribe(self, callback: Subscriber) -> Callable[[], None]:
        if not callable(callback):
            raise TypeError("subscriber must be callable")

        self._subscribers.append(callback)

        def unsubscribe() -> None:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

        return unsubscribe

    def __repr__(self) -> str:
        return f"State({self._value!r})"
