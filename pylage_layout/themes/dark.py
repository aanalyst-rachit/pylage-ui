"""Dark theme preset for PyLage Layout."""

from .factory import create_theme


DARK_COLORS = {
    "background": "#0f172a",
    "surface": "#1e293b",
    "surface_alt": "#334155",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "border": "#475569",
    "primary": "#60a5fa",
    "secondary": "#94a3b8",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "info": "#38bdf8",
}

DARK_THEME = create_theme(
    name="dark",
    colors=DARK_COLORS,
)

__all__ = ["DARK_COLORS", "DARK_THEME"]
