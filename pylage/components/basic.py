from __future__ import annotations

from typing import Any

from pylage.core.component import Component, component
from pylage.core.state import State


def Text(text: Any, **props: Any) -> Component:
    return component("Text", text=text, **props)


def Column(*children, **props: Any) -> Component:
    return component("Column", *children, **props)


def Row(*children, **props: Any) -> Component:
    return component("Row", *children, **props)


def Card(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Card"):
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

    return component("Card", *children, **props)



def Divider(*children, **props: Any) -> Component:
    return component("Divider", *children, **props)

def Badge(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Badge"):
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

    return component("Badge", *children, **props)


def Avatar(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Avatar"):
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

    return component("Avatar", *children, **props)


def Accordion(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Accordion"):
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

    return component("Accordion", *children, **props)


def Carousel(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Carousel"):
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

    return component("Carousel", *children, **props)


def Grid(*children, **props: Any) -> Component:
    return component("Grid", *children, **props)


def Image(**props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Image"):
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

    return component("Image", **props)


def Video(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Video"):
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

    return component("Video", *children, **props)


def Audio(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Audio"):
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

    return component("Audio", *children, **props)


def Icon(**props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Icon"):
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

    return component("Icon", **props)


def Canvas(*children, **props: Any) -> Component:
    from pylage.core.registry import PropDefinition, registry

    if not registry.has("Canvas"):
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

    return component("Canvas", *children, **props)


def Heading(text: Any, **props: Any) -> Component:
    return component("Heading", text=text, **props)


def Button(text: Any, **props: Any) -> Component:
    return component("Button", text=text, **props)


def Input(
    value: Any = "",
    input_type: str | None = None,
    **props: Any,
) -> Component:
    if input_type is not None:
        props["_html_type"] = input_type

    if isinstance(value, State) and "on_input" not in props:
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

        props["on_input"] = update_state

    return component("Input", value=value, **props)


def Form(*children, **props: Any) -> Component:
    return component("Form", *children, **props)


def Table(*children, **props: Any) -> Component:
    return component("Table", *children, **props)


def Dialog(*children, **props: Any) -> Component:
    return component("Dialog", *children, **props)


def Navigation(*children, **props: Any) -> Component:
    return component("Navigation", *children, **props)


def Tabs(*children, **props: Any) -> Component:
    return component("Tabs", *children, **props)


def Checkbox(**props: Any) -> Component:
    return component("Checkbox", **props)


def RadioGroup(*children, **props: Any) -> Component:
    return component("RadioGroup", *children, **props)


def Switch(**props: Any) -> Component:
    return component("Switch", **props)


def Select(*children, **props: Any) -> Component:
    return component("Select", *children, **props)


def Option(text: Any, value: Any = None, **props: Any) -> Component:
    if value is not None:
        props["value"] = value

    return component("Option", text=text, **props)


def Slider(**props: Any) -> Component:
    return component("Slider", **props)


def DatePicker(**props: Any) -> Component:
    return component("DatePicker", **props)


def Alert(*children, **props: Any) -> Component:
    return component("Alert", *children, **props)


def Toast(*children, **props: Any) -> Component:
    return component("Toast", *children, **props)


def Spinner(*children, **props: Any) -> Component:
    return component("Spinner", *children, **props)


def ProgressBar(*children, **props: Any) -> Component:
    return component("ProgressBar", *children, **props)


def Skeleton(*children, **props: Any) -> Component:
    return component("Skeleton", *children, **props)


def Breadcrumbs(*children, **props: Any) -> Component:
    return component("Breadcrumbs", *children, **props)


def Pagination(*children, **props: Any) -> Component:
    return component("Pagination", *children, **props)


def Menu(*children, **props: Any) -> Component:
    return component("Menu", *children, **props)


def Drawer(*children, **props: Any) -> Component:
    return component("Drawer", *children, **props)


def Tooltip(*children, **props: Any) -> Component:
    return component("Tooltip", *children, **props)


def Popover(*children, **props: Any) -> Component:
    return component("Popover", *children, **props)
