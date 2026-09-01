from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Style:
    """Structured CSS style definition for PyLage components."""

    color: Any = None
    background: Any = None
    background_color: Any = None

    font_size: Any = None
    font_weight: Any = None
    font_family: Any = None
    line_height: Any = None
    text_align: Any = None

    margin: Any = None
    margin_top: Any = None
    margin_right: Any = None
    margin_bottom: Any = None
    margin_left: Any = None

    padding: Any = None
    padding_top: Any = None
    padding_right: Any = None
    padding_bottom: Any = None
    padding_left: Any = None

    width: Any = None
    min_width: Any = None
    max_width: Any = None

    height: Any = None
    min_height: Any = None
    max_height: Any = None

    display: Any = None
    position: Any = None
    top: Any = None
    right: Any = None
    bottom: Any = None
    left: Any = None

    flex_direction: Any = None
    flex_wrap: Any = None
    justify_content: Any = None
    align_items: Any = None
    align_content: Any = None
    flex: Any = None
    flex_grow: Any = None
    flex_shrink: Any = None
    flex_basis: Any = None

    gap: Any = None
    row_gap: Any = None
    column_gap: Any = None

    grid_template_columns: Any = None
    grid_template_rows: Any = None
    grid_column: Any = None
    grid_row: Any = None

    border: Any = None
    border_width: Any = None
    border_style: Any = None
    border_color: Any = None
    border_radius: Any = None

    box_shadow: Any = None
    opacity: Any = None
    overflow: Any = None
    box_sizing: Any = None
    cursor: Any = None

    custom: dict[str, Any] | None = None

    def merge(self, override: "Style | None") -> "Style":
        """Return a new Style with override values taking precedence."""

        if override is None:
            return self

        if not isinstance(override, Style):
            raise TypeError("override must be a Style or None")

        values = {}

        for field_name in self.__dataclass_fields__:
            if field_name == "custom":
                continue

            value = getattr(override, field_name)

            if value is None:
                value = getattr(self, field_name)

            values[field_name] = value

        custom = dict(self.custom or {})
        custom.update(override.custom or {})
        values["custom"] = custom or None

        return Style(**values)

    def to_css(self) -> str:
        """Convert the style definition into a CSS declaration string."""

        # Import lazily to avoid a styling -> core import cycle.
        from pylage.core.state import State

        declarations: list[str] = []

        for field_name, value in self.__dict__.items():
            if field_name == "custom":
                continue

            if isinstance(value, State):
                value = value.value

            if value is None:
                continue

            css_name = _css_name(field_name)
            declarations.append(
                f"{css_name}:{value}"
            )

        for name, value in (self.custom or {}).items():
            if isinstance(value, State):
                value = value.value

            if value is None:
                continue

            if not isinstance(name, str) or not name.startswith("--"):
                raise ValueError(
                    "custom CSS property names must start with '--'"
                )

            declarations.append(
                f"{name}:{value}"
            )

        return ";".join(declarations)


def _css_name(name: str) -> str:
    """Convert Python snake_case names into CSS kebab-case names."""

    return name.replace("_", "-")
