from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
import uuid

from pylage.core.registry import registry


Child = Any
EventHandler = Callable[..., Any]
MutationSubscriber = Callable[[dict[str, Any]], None]


@dataclass
class Component:
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Child] = field(default_factory=list)
    events: dict[str, EventHandler] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    _parent: Component | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _mutation_subscribers: list[MutationSubscriber] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def add(self, *children: Child) -> "Component":
        for child in children:
            if isinstance(child, Component):
                if child is self:
                    raise ValueError(
                        "A component cannot contain itself."
                    )

                ancestor = self
                while ancestor is not None:
                    if ancestor is child:
                        raise ValueError(
                            "A component cannot contain an ancestor."
                        )
                    ancestor = ancestor._parent

                if child._parent is not None:
                    old_parent = child._parent

                    if child in old_parent.children:
                        old_parent.children.remove(child)

                child._parent = self

        self.children.extend(children)

        event = {
            "type": "add",
            "parent": self,
            "children": list(children),
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def remove(self, child: Child) -> "Component":
        """Remove a child and notify mutation subscribers."""

        try:
            self.children.remove(child)
        except ValueError:
            raise ValueError(
                "Child is not present in this component."
            ) from None

        if isinstance(child, Component):
            child._parent = None

        event = {
            "type": "remove",
            "parent": self,
            "children": [child],
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def move_to(self, new_parent: "Component") -> "Component":
        if not isinstance(new_parent, Component):
            raise TypeError(
                "move_to expects a Component parent."
            )

        if self is new_parent:
            raise ValueError(
                "A component cannot be moved into itself."
            )

        old_parent = self._parent

        if old_parent is None:
            raise ValueError(
                "Component is not attached to a parent."
            )

        if self not in old_parent.children:
            raise ValueError(
                "Component parent relationship is inconsistent."
            )

        old_parent.children.remove(self)
        self._parent = new_parent
        new_parent.children.append(self)

        event = {
            "type": "move",
            "component": self,
            "old_parent": old_parent,
            "new_parent": new_parent,
        }

        for subscriber in tuple(
            new_parent._mutation_subscribers
        ):
            subscriber(event)

        return self

    def insert(
        self,
        index: int,
        *children: Child,
    ) -> "Component":
        if not isinstance(index, int):
            raise TypeError(
                "insert index must be an integer."
            )

        if not children:
            raise ValueError(
                "insert requires at least one child."
            )

        normalized_index = index

        for child in children:
            if isinstance(child, Component):
                if child is self:
                    raise ValueError(
                        "A component cannot contain itself."
                    )

                ancestor = self
                while ancestor is not None:
                    if ancestor is child:
                        raise ValueError(
                            "A component cannot contain an ancestor."
                        )
                    ancestor = ancestor._parent

                if child._parent is not None:
                    old_parent = child._parent

                    if child in old_parent.children:
                        old_parent.children.remove(child)

        for offset, child in enumerate(children):
            self.children.insert(
                normalized_index + offset,
                child,
            )

            if isinstance(child, Component):
                child._parent = self

        event = {
            "type": "add",
            "parent": self,
            "children": list(children),
            "index": normalized_index,
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def replace(
        self,
        old_child: Child,
        new_child: Child,
    ) -> "Component":
        try:
            index = self.children.index(old_child)
        except ValueError as exc:
            raise ValueError(
                "Child is not attached to this parent."
            ) from exc

        if isinstance(new_child, Component):
            if new_child is self:
                raise ValueError(
                    "A component cannot contain itself."
                )

            ancestor = self
            while ancestor is not None:
                if new_child is ancestor:
                    raise ValueError(
                        "A component cannot contain an ancestor."
                    )
                ancestor = getattr(ancestor, "_parent", None)

            old_parent = getattr(new_child, "_parent", None)

            if old_parent is not None and new_child in old_parent.children:
                old_parent.children.remove(new_child)

        self.children[index] = new_child

        if isinstance(old_child, Component):
            old_child._parent = None

        if isinstance(new_child, Component):
            new_child._parent = self

        event = {
            "type": "replace",
            "parent": self,
            "old_child": old_child,
            "new_child": new_child,
            "index": index,
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def clear(self) -> "Component":
        removed_children = list(self.children)

        if not removed_children:
            return self

        self.children.clear()

        for child in removed_children:
            if isinstance(child, Component):
                child._parent = None

        event = {
            "type": "clear",
            "parent": self,
            "children": removed_children,
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def set_children(
        self,
        *children: Child,
    ) -> "Component":
        for child in children:
            if isinstance(child, Component):
                if child is self:
                    raise ValueError(
                        "A component cannot contain itself."
                    )

                ancestor = self
                while ancestor is not None:
                    if child is ancestor:
                        raise ValueError(
                            "A component cannot contain an ancestor."
                        )
                    ancestor = getattr(ancestor, "_parent", None)

        old_children = list(self.children)

        for child in children:
            if isinstance(child, Component):
                old_parent = getattr(child, "_parent", None)

                if (
                    old_parent is not None
                    and old_parent is not self
                    and child in old_parent.children
                ):
                    old_parent.children.remove(child)

        self.children = list(children)

        for child in old_children:
            if isinstance(child, Component):
                child._parent = None

        for child in self.children:
            if isinstance(child, Component):
                child._parent = self

        event = {
            "type": "set_children",
            "parent": self,
            "old_children": old_children,
            "children": list(self.children),
        }

        for subscriber in tuple(self._mutation_subscribers):
            subscriber(event)

        return self

    def subscribe_mutation(
        self,
        callback: MutationSubscriber,
    ) -> Callable[[], None]:
        if not callable(callback):
            raise TypeError("mutation subscriber must be callable")

        self._mutation_subscribers.append(callback)

        def unsubscribe() -> None:
            if callback in self._mutation_subscribers:
                self._mutation_subscribers.remove(callback)

        return unsubscribe

    def on(
        self,
        event: str,
        handler: EventHandler,
    ) -> "Component":
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string")

        if not callable(handler):
            raise TypeError("handler must be callable")

        self.events[event] = handler
        return self

    def __repr__(self) -> str:
        return (
            f"Component("
            f"type={self.type!r}, "
            f"id={self.id!r}, "
            f"props={self.props!r}, "
            f"children={self.children!r}, "
            f"events={list(self.events)!r})"
        )


def component(
    type: str,
    *children: Child,
    **props: Any,
) -> Component:
    normalized_children = [
        child for child in children
        if child is not None
    ]

    events: dict[str, EventHandler] = {}

    event_props = {
        key: value
        for key, value in props.items()
        if key.startswith("on_")
    }

    for key in event_props:
        props.pop(key)

    for key, handler in event_props.items():
        event_name = key[3:]

        if not callable(handler):
            raise TypeError(
                f"{key} must be callable"
            )

        events[event_name] = handler

    # Consult the registry when a component type is known.
    #
    # The registry currently provides metadata and contracts for known
    # components, while unknown components remain backward-compatible.
    definition = registry.get(type)

    if definition is not None and definition.props is not None:
        # Keep all supplied props for compatibility. Registry metadata
        # is authoritative for known properties but does not yet reject
        # unknown properties.
        normalized_props = dict(props)
    else:
        normalized_props = dict(props)

    return Component(
        type=type,
        props=normalized_props,
        children=normalized_children,
        events=events,
    )
