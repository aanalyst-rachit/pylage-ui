from __future__ import annotations

from html import escape
from typing import Any

from pylage.core.component import Component
from pylage.core.state import State
from pylage.core.registry import registry
from pylage.styling import Style


class HTMLRenderer:
    """Render a PyLage component tree into HTML."""

    def __init__(
        self,
        registry_instance=None,
        theme=None,
    ) -> None:
        self._registry = registry_instance or registry
        self._theme = theme
        self._register_builtin_renderers()

    @property
    def registry(self):
        return self._registry

    def _register_builtin_renderers(self) -> None:
        """Attach built-in rendering callbacks to registry definitions."""

        builtins = {
            "Column": lambda renderer, component:
                renderer._render_column(component),

            "Row": lambda renderer, component:
                renderer._render_row(component),

            "Dialog": lambda renderer, component:
                renderer._render_dialog(component),

            "Table": lambda renderer, component:
                renderer._render_table(component),

            "Form": lambda renderer, component:
                renderer._render_form(component),

            "Card": lambda renderer, component:
                renderer._render_card(component),

            "Text": lambda renderer, component:
                renderer._render_text(component),

            "Heading": lambda renderer, component:
                renderer._render_heading(component),

            "Breadcrumbs": lambda renderer, component:
                renderer._render_breadcrumbs(component),

            "Button": lambda renderer, component:
                renderer._render_button(component),

            "Input": lambda renderer, component:
                renderer._render_input(component),
        }

        for component_type, renderer_callback in builtins.items():
            definition = self.registry.get(component_type)

            if definition is None:
                continue

            if definition.renderer is not None:
                continue

            self.registry.set_renderer(
                component_type,
                renderer_callback,
            )

    def _value(self, value: Any) -> Any:
        """Resolve reactive State values."""
        if isinstance(value, State):
            return value.value
        return value

    def render(self, component: Component) -> str:
        html = self._render_component(component)

        if self._theme is not None:
            theme_css = self._theme.to_css()

            if theme_css:
                html = (
                    f"<style>:root{{{theme_css}}}</style>"
                    + html
                )

        return html

    def _event_attributes(self, component: Component) -> str:
        if not component.events:
            return ""

        events = ",".join(
            escape(event, quote=True)
            for event in component.events
        )

        return f' data-pylage-events="{events}"'

    def _render_children(self, component: Component) -> str:
        return "".join(
            self._render_component(child)
            for child in component.children
            if isinstance(child, Component)
        )

    def _render_common_attributes(
        self,
        component: Component,
        default_style: Style | None = None,
    ) -> str:
        component_id = escape(component.id, quote=True)

        attributes = (
            f'data-pylage-id="{component_id}"'
            f'{self._event_attributes(component)}'
        )

        style = component.props.get("style")

        if isinstance(style, State):
            style = style.value

        if default_style is not None:
            if style is None:
                style = default_style
            elif isinstance(style, Style):
                style = default_style.merge(style)

        if style is not None:
            to_css = getattr(style, "to_css", None)

            if callable(to_css):
                css = to_css()

                if css:
                    attributes += (
                        f' style="{escape(css, quote=True)}"'
                    )

        return attributes

    def _render_prop_attributes(
        self,
        component: Component,
        excluded: set[str] | None = None,
    ) -> str:
        """Render component props using registry metadata."""
        excluded = excluded or set()

        definition = self.registry.get(component.type)

        # Input-like components with fixed HTML input types.
        if component.type in {"Checkbox", "Switch"}:
            component.props.setdefault("_html_type", "checkbox")
        elif component.type == "Slider":
            component.props.setdefault("_html_type", "range")
        elif component.type == "DatePicker":
            component.props.setdefault("_html_type", "date")

        prop_definitions = (
            definition.props
            if definition is not None and definition.props is not None
            else {}
        )

        attributes: list[str] = []

        for name, raw_value in component.props.items():
            # ``style`` is rendered by _render_common_attributes().
            # Never emit it again as a generic HTML attribute.
            if name == "style" or name in excluded:
                continue

            value = self._value(raw_value)

            if value is None:
                continue

            prop_definition = prop_definitions.get(name)

            if name == "_html_type":
                html_name = "type"
                kind = "attribute"
            # Registry metadata controls the HTML attribute name.
            if prop_definition is not None:
                html_name = prop_definition.html_name or name
                kind = prop_definition.kind
            else:
                # Unknown props remain backward-compatible.
                # HTML naming is owned by registry metadata.
                html_name = name
                kind = "attribute"

            if name == "_html_type":
                attributes.append(
                    f'type="{escape(str(value), quote=True)}"'
                )
                continue

            if kind == "boolean":
                if value:
                    attributes.append(
                        escape(html_name, quote=True)
                    )
                continue

            if kind == "text":
                continue

            if value is True:
                attributes.append(
                    escape(html_name, quote=True)
                )
                continue

            attributes.append(
                f'{escape(html_name, quote=True)}='
                f'"{escape(str(value), quote=True)}"'
            )

        if not attributes:
            return ""

        return " " + " ".join(attributes)

    def _render_form(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        attributes = common + self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f"<form {attributes}>"
            f"{children}"
            f"</form>"
        )

    def _render_table(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        attributes = common + self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f"<table {attributes}>"
            f"{children}"
            f"</table>"
        )

    def _render_dialog(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        attributes = common + self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f"<dialog {attributes}>"
            f"{children}"
            f"</dialog>"
        )

    def _render_column(self, component: Component) -> str:
        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="flex",
                flex_direction="column",
            ),
        )
        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        definition = self.registry.get(component.type)
        tag = definition.tag if definition is not None else "div"

        return (
            f'<{tag} {common}{props}>'
            f'{children}</{tag}>'
        )

    def _render_row(self, component: Component) -> str:
        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="flex",
                flex_direction="row",
            ),
        )
        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f'<div {common}{props}>'
            f'{children}</div>'
        )

    def _render_card(self, component: Component) -> str:
        """Render Card using its registry-defined HTML tag."""

        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="block",
                width="100%",
                box_sizing="border-box",
            ),
        )

        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )

        children = self._render_children(component)

        # Registry-defined text props become element content.
        text_values: list[str] = []

        definition = self.registry.get(component.type)

        if definition is not None and definition.props is not None:
            for prop_name, prop_definition in definition.props.items():
                if prop_definition.kind != "text":
                    continue

                value = component.props.get(prop_name)

                if value is None:
                    continue

                value = self._value(value)

                if value is not None:
                    text_values.append(escape(str(value)))

        if text_values:
            children = "".join(text_values) + children

        tag = definition.tag if definition is not None else "div"

        return (
            f'<{tag} {common}{props}>'
            f'{children}</{tag}>'
        )


    def _render_text(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "")
        )

        return (
            f"<div {common}>"
            f"{escape(str(text))}"
            f"</div>"
        )

    def _render_heading(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "")
        )

        definition = self.registry.get("Heading")
        tag = definition.tag if definition is not None else "h1"

        return (
            f"<{tag} {common}>"
            f"{escape(str(text))}"
            f"</{tag}>"
        )

    def _render_breadcrumbs(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        attributes = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        if attributes:
            attributes = " " + attributes

        items = "".join(
            f"<li>{self._render_component(child)}</li>"
            for child in component.children
            if isinstance(child, Component)
        )

        return (
            f'<nav {common}{attributes} aria-label="Breadcrumb">'
            f"<ol>{items}</ol>"
            f"</nav>"
        )

    def _render_input(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        if component.events:
            events = self._event_attributes(component)
        else:
            events = ' data-pylage-events="input,change"'

        attributes = self._render_prop_attributes(
            component,
            excluded={"children"},
        )

        if component.type == "Slider":
            attributes += ' type="range"'

        return (
            f"<input {common}{events}"
            f"{attributes}>"
        )

    def _render_button(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "Button")
        )

        attributes = common + self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        return (
            f"<button {attributes}>"
            f"{escape(str(text))}"
            f"</button>"
        )

    def _render_component(self, component: Component) -> str:
        component_type = component.type

        definition = self.registry.get(component_type)

        if definition is None:
            tag = "div"
        else:
            tag = definition.tag

        common = self._render_common_attributes(component)
        children = self._render_children(component)

        # ---------------------------------------------------------
        # Custom registered renderer
        # ---------------------------------------------------------
        if definition is not None and definition.renderer is not None:
            return definition.renderer(self, component)

        # ---------------------------------------------------------
        # Generic component
        # ---------------------------------------------------------
        # Unknown components still render instead of disappearing.
        # Their children and normal props remain available.
        generic_attributes = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        # Slider is rendered as an HTML range input.
        if component.type == "Slider":
            generic_attributes += ' type="range"'

        if definition is not None and definition.void:
            return (
                f"<{tag} {common}"
                f"{generic_attributes}>"
            )

        # Registry-defined text props become component content.
        text_values: list[str] = []

        if definition is not None and definition.props is not None:
            for prop_name, prop_definition in definition.props.items():
                if prop_definition.kind != "text":
                    continue

                value = component.props.get(prop_name)

                if value is None:
                    continue

                value = self._value(value)

                if value is not None:
                    text_values.append(escape(str(value)))

        # Backward-compatible generic text support.
        # A registered custom component such as:
        #     registry.register("Card", "section")
        # may provide props={"text": "Hello Card"} without
        # explicitly declaring a text PropDefinition.
        if not text_values and "text" in component.props:
            value = self._value(component.props.get("text"))

            if value is not None:
                text_values.append(escape(str(value)))

        if text_values:
            children = "".join(text_values) + children

        return (
            f"<{tag} {common}"
            f"{generic_attributes}>"
            f"{children}"
            f"</{tag}>"
        )


def render(component: Component) -> str:
    """Convenience function for rendering a component tree."""
    return HTMLRenderer().render(component)
