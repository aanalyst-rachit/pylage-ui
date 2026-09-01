from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class PropDefinition:
    """Definition of a component property."""

    name: str
    kind: str = "attribute"
    reactive: bool = True
    html_name: str | None = None


@dataclass(frozen=True)
class ComponentDefinition:
    """Rendering definition for a PyLage component."""

    type: str
    tag: str
    void: bool = False
    renderer: Callable[..., str] | None = None
    props: dict[str, PropDefinition] | None = None


class ComponentRegistry:
    """Registry of known PyLage component rendering definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, ComponentDefinition] = {}

    def register(
        self,
        type: str,
        tag: str,
        *,
        void: bool = False,
        renderer: Callable[..., str] | None = None,
        props: dict[str, PropDefinition] | None = None,
    ) -> ComponentDefinition:
        if not isinstance(type, str) or not type:
            raise ValueError(
                "component type must be a non-empty string"
            )

        if not isinstance(tag, str) or not tag:
            raise ValueError(
                "component tag must be a non-empty string"
            )

        if props is not None:
            props = dict(props)

            for name, definition in props.items():
                if not isinstance(name, str) or not name:
                    raise ValueError(
                        "prop name must be a non-empty string"
                    )

                if not isinstance(definition, PropDefinition):
                    raise TypeError(
                        f"prop {name!r} must be a PropDefinition"
                    )

                if definition.name != name:
                    raise ValueError(
                        f"prop definition name mismatch: "
                        f"{name!r} != {definition.name!r}"
                    )


                if definition.html_name is not None:
                    if not isinstance(definition.html_name, str):
                        raise TypeError(
                            f"html_name must be a string or None, "
                            f"got {type(definition.html_name).__name__}"
                        )

                    if not definition.html_name:
                        raise ValueError(
                            "html_name must be a non-empty string"
                        )
                if not isinstance(definition.reactive, bool):
                    raise TypeError(
                        f"reactive must be a bool, "
                        f"got {type(definition.reactive).__name__}"
                    )

                if definition.kind not in {
                    "attribute",
                    "boolean",
                    "text",
                }:
                    raise ValueError(
                        f"unsupported prop kind: "
                        f"{definition.kind!r}"
                    )

        definition = ComponentDefinition(
            type=type,
            tag=tag,
            void=void,
            renderer=renderer,
            props=props,
        )

        self._definitions[type] = definition
        return definition

    def get(self, type: str) -> ComponentDefinition | None:
        return self._definitions.get(type)

    def set_renderer(
        self,
        type: str,
        renderer: Callable[..., str],
    ) -> ComponentDefinition:
        """Attach a renderer without changing the component contract."""

        definition = self.require(type)

        if not callable(renderer):
            raise TypeError("renderer must be callable")

        updated = ComponentDefinition(
            type=definition.type,
            tag=definition.tag,
            void=definition.void,
            renderer=renderer,
            props=definition.props,
        )

        self._definitions[type] = updated
        return updated

    def require(self, type: str) -> ComponentDefinition:
        definition = self.get(type)

        if definition is None:
            raise KeyError(
                f"Unknown component type: {type!r}"
            )

        return definition

    def has(self, type: str) -> bool:
        return type in self._definitions

    def unregister(self, type: str) -> None:
        self._definitions.pop(type, None)

    def types(self) -> tuple[str, ...]:
        return tuple(self._definitions)


registry = ComponentRegistry()


# Built-in PyLage component definitions.
#
# Text is a first-class UI component. Its text prop becomes
# the rendered element content.

registry.register(
    "Text",
    "div",
    props={
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)

#
registry.register(
    "Card",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)
registry.register(
    "Tabs",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)


registry.register(
    "DatePicker",
    "input",
    void=True,
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "min": PropDefinition(
            "min",
            kind="attribute",
            html_name="min",
        ),
        "max": PropDefinition(
            "max",
            kind="attribute",
            html_name="max",
        ),
    },
)



registry.register(
    "Alert",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)



registry.register(
    "Toast",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)



registry.register(
    "Spinner",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)



registry.register(
    "ProgressBar",
    "progress",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "max": PropDefinition(
            "max",
            kind="attribute",
            html_name="max",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)



registry.register(
    "Skeleton",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)



registry.register(
    "Breadcrumbs",
    "nav",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)



registry.register(
    "Pagination",
    "nav",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)



registry.register(
    "Menu",
    "menu",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)



registry.register(
    "Drawer",
    "aside",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)



registry.register(
    "Tooltip",
    "span",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)



registry.register(
    "Popover",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)


# Rendering behavior lives in HTMLRenderer, while the registry
# owns the public component -> HTML tag + prop contract.
registry.register(
    "RadioGroup",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Switch",
    "input",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "checked": PropDefinition(
            "checked",
            kind="boolean",
            html_name="checked",
        ),
    },
)

registry.register(
    "Select",
    "select",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "multiple": PropDefinition(
            "multiple",
            kind="boolean",
            html_name="multiple",
        ),
    },
)

registry.register(
    "Option",
    "option",
    props={
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)


registry.register(
    "Slider",
    "input",
    void=True,
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "min": PropDefinition(
            "min",
            kind="attribute",
            html_name="min",
        ),
        "max": PropDefinition(
            "max",
            kind="attribute",
            html_name="max",
        ),
        "step": PropDefinition(
            "step",
            kind="attribute",
            html_name="step",
        ),
    },
)

registry.register(
    "Form",
    "form",
)

registry.register(
    "Table",
    "table",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Dialog",
    "dialog",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Navigation",
    "nav",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Checkbox",
    "input",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "checked": PropDefinition(
            "checked",
            kind="boolean",
            html_name="checked",
        ),
    },
)


registry.register(
    "Divider",
    "hr",
    void=True,
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Row",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Grid",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Column",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)


registry.register(
    "Badge",
    "span",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Avatar",
    "span",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Accordion",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Carousel",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Image",
    "img",
    void=True,
    props={
        "src": PropDefinition(
            "src",
            kind="attribute",
            html_name="src",
        ),
        "alt": PropDefinition(
            "alt",
            kind="attribute",
            html_name="alt",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Video",
    "video",
    props={
        "src": PropDefinition(
            "src",
            kind="attribute",
            html_name="src",
        ),
        "controls": PropDefinition(
            "controls",
            kind="boolean",
            html_name="controls",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Audio",
    "audio",
    props={
        "src": PropDefinition(
            "src",
            kind="attribute",
            html_name="src",
        ),
        "controls": PropDefinition(
            "controls",
            kind="boolean",
            html_name="controls",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Icon",
    "span",
    props={
        "name": PropDefinition(
            "name",
            kind="text",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Canvas",
    "svg",
    props={
        "width": PropDefinition(
            "width",
            kind="attribute",
            html_name="width",
        ),
        "height": PropDefinition(
            "height",
            kind="attribute",
            html_name="height",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Heading",
    "h1",
    props={
        "text": PropDefinition(
            "text",
            kind="text",
        ),
    },
)

registry.register(
    "Button",
    "button",
    props={
        "text": PropDefinition(
            "text",
            kind="text",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "disabled": PropDefinition(
            "disabled",
            kind="boolean",
            html_name="disabled",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)

registry.register(
    "Input",
    "input",
    void=True,
    props={
        "value": PropDefinition(
            "value",
            kind="attribute",
            html_name="value",
        ),
        "disabled": PropDefinition(
            "disabled",
            kind="boolean",
            html_name="disabled",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
    },
)


__all__ = [
    "PropDefinition",
    "ComponentDefinition",
    "ComponentRegistry",
    "registry",
]
