import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps
from pylage import Style


def get_app():
    # -------------------------------------------------------------------------
    # State Management
    # -------------------------------------------------------------------------
    dark_mode = ps.State(False)
    notifications_enabled = ps.State(False)

    # State Inverter Handlers
    def toggle_dark_mode(val=None):
        dark_mode.set(not dark_mode.value)

    def toggle_notifications(val=None):
        notifications_enabled.set(not notifications_enabled.value)

    # Clean Safe Checkbox Constructor (Avoids duplicate 'type' parameter conflict)
    def create_checkbox(checked_val, click_handler):
        # 1. Preferred Native PyLage Checkbox Component
        if hasattr(ps, "Checkbox"):
            return ps.Checkbox(
                value=checked_val,
                on_change=click_handler,
                style=Style(width="18px", height="18px", cursor="pointer")
            )
        
        # 2. Safe Fallback using generic PyLage Component engine
        from pylage.core.component import Component
        chk = Component("input")
        chk.props["type"] = "checkbox"
        chk.props["checked"] = checked_val
        chk.on("click", click_handler)
        chk.on("change", click_handler)
        return chk

    # -------------------------------------------------------------------------
    # UI Component Tree Return
    # -------------------------------------------------------------------------
    return ps.Column(
        # Page Title
        ps.Heading(
            "Switch Component Demo",
            style=Style(
                font_size="1.75rem",
                font_weight="800",
                color="#0f172a",
                margin_bottom="0.25rem",
            ),
        ),
        ps.Text(
            "Interactive demonstration of toggle states in PyLage.",
            style=Style(color="#64748b", font_size="0.9rem", margin_bottom="1.5rem"),
        ),

        # ---------------------------------------------------------------------
        # DEMO 1: Dark Mode Toggle
        # ---------------------------------------------------------------------
        ps.Column(
            ps.Row(
                ps.Text("Dark Theme: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(dark_mode, style=Style(color="#2563eb", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            ps.Row(
                create_checkbox(dark_mode.value, toggle_dark_mode),
                ps.Text("Enable Dark Theme", style=Style(color="#334155", font_size="0.95rem", cursor="pointer")),
                style=Style(gap="0.75rem", align_items="center"),
            ),
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1rem",
                width="100%",
            ),
        ),

        # ---------------------------------------------------------------------
        # DEMO 2: Notifications Toggle
        # ---------------------------------------------------------------------
        ps.Column(
            ps.Row(
                ps.Text("Notifications: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(notifications_enabled, style=Style(color="#059669", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            ps.Row(
                create_checkbox(notifications_enabled.value, toggle_notifications),
                ps.Text("Allow Email Notifications", style=Style(color="#334155", font_size="0.95rem", cursor="pointer")),
                style=Style(gap="0.75rem", align_items="center"),
            ),
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                width="100%",
            ),
        ),

        # Outer Layout Styling
        style=Style(
            width="100%",
            max_width="560px",
            padding="2rem",
            background_color="#f8fafc",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )