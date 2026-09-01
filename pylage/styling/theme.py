from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class Theme:
    """Immutable design-token theme for PyLage."""

    name: str = "default"
    colors: Mapping[str, Any] = field(default_factory=dict)
    spacing: Mapping[str, Any] = field(default_factory=dict)
    radius: Mapping[str, Any] = field(default_factory=dict)
    fonts: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "colors", MappingProxyType(dict(self.colors)))
        object.__setattr__(self, "spacing", MappingProxyType(dict(self.spacing)))
        object.__setattr__(self, "radius", MappingProxyType(dict(self.radius)))
        object.__setattr__(self, "fonts", MappingProxyType(dict(self.fonts)))

    def color(self, name: str) -> Any:
        return self._get(self.colors, name, "color")

    def spacing_value(self, name: str) -> Any:
        return self._get(self.spacing, name, "spacing")

    def radius_value(self, name: str) -> Any:
        return self._get(self.radius, name, "radius")

    def font(self, name: str) -> Any:
        return self._get(self.fonts, name, "font")

    def to_css(self) -> str:
        """Generate CSS custom-property declarations."""

        declarations: list[str] = []

        sections = (
            ("color", self.colors),
            ("spacing", self.spacing),
            ("radius", self.radius),
            ("font", self.fonts),
        )

        for prefix, tokens in sections:
            for name, value in tokens.items():
                if value is None:
                    continue

                declarations.append(
                    f"--{prefix}-{_css_name(name)}:{value}"
                )

        return ";".join(declarations)

    @staticmethod
    def _get(
        tokens: Mapping[str, Any],
        name: str,
        category: str,
    ) -> Any:
        if name not in tokens:
            raise KeyError(
                f"Unknown {category} token: {name!r}"
            )

        return tokens[name]


def _css_name(name: str) -> str:
    """Convert snake_case token names into kebab-case."""

    return name.replace("_", "-")
