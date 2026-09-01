from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pylage.styling.style import Style


@dataclass(frozen=True)
class ResponsiveStyle:
    """Immutable responsive style definition."""

    base: Style | None = None
    sm: Style | None = None
    md: Style | None = None
    lg: Style | None = None
    xl: Style | None = None

    BREAKPOINTS = {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
    }

    def to_css(self) -> str:
        """Generate responsive CSS media-query blocks."""

        blocks: list[str] = []

        if self.base is not None:
            css = self.base.to_css()
            if css:
                blocks.append(css)

        for name in ("sm", "md", "lg", "xl"):
            style = getattr(self, name)

            if style is None:
                continue

            css = style.to_css()

            if not css:
                continue

            breakpoint = self.BREAKPOINTS[name]

            blocks.append(
                f"@media (min-width:{breakpoint}){{{css}}}"
            )

        return "".join(blocks)

    def to_base_css(self) -> str:
        """Return only the base Style CSS declarations."""

        if self.base is None:
            return ""

        return self.base.to_css()

    def to_responsive_css(self, selector: str) -> str:
        """Return only breakpoint-specific CSS rules."""

        blocks: list[str] = []

        for name in ("sm", "md", "lg", "xl"):
            style = getattr(self, name)

            if style is None:
                continue

            css = style.to_css()

            if not css:
                continue

            breakpoint = self.BREAKPOINTS[name]

            blocks.append(
                f"@media (min-width:{breakpoint}){{{selector}{{{css}}}}}"
            )

        return "".join(blocks)

