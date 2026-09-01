import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps
from pylage import Style

def get_app():
    # Dynamic State for Row Interactivity Demo
    active_tab = ps.State("Home")

    def select_home():
        active_tab.set("Home")

    def select_profile():
        active_tab.set("Profile")

    def select_settings():
        active_tab.set("Settings")

    # Helper function for dummy boxes
    def create_box(text, bg_color="#2563eb", width="80px", height="50px"):
        return ps.Column(
            ps.Text(text, style=Style(color="#ffffff", font_weight="700")),
            style=Style(
                background_color=bg_color,
                width=width,
                height=height,
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="0.375rem",
            ),
        )

    # ============================================================
    # 1. BASIC ROW WITH GAP
    # ============================================================
    basic_row = ps.Row(
        create_box("Box 1", "#2563eb"),
        create_box("Box 2", "#7c3aed"),
        create_box("Box 3", "#dc2626"),
        style=Style(
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 2. JUSTIFY CONTENT (Space Between)
    # ============================================================
    justify_row = ps.Row(
        create_box("Left", "#059669"),
        create_box("Center", "#d97706"),
        create_box("Right", "#2563eb"),
        style=Style(
            justify_content="space-between",
            align_items="center",
            width="100%",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 3. ALIGN ITEMS (Vertical Alignment)
    # ============================================================
    align_row = ps.Row(
        create_box("Tall", "#7c3aed", height="80px"),
        create_box("Short", "#2563eb", height="40px"),
        create_box("Medium", "#059669", height="60px"),
        style=Style(
            align_items="center",
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 4. FLEX WRAP DEMO
    # ============================================================
    wrap_row = ps.Row(
        create_box("Item 1", "#2563eb", width="150px"),
        create_box("Item 2", "#7c3aed", width="150px"),
        create_box("Item 3", "#dc2626", width="150px"),
        create_box("Item 4", "#059669", width="150px"),
        style=Style(
            flex_wrap="wrap",
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 5. INTERACTIVE NAVIGATION ROW (State Triggering)
    # ============================================================
    nav_row = ps.Row(
        ps.Button("Home", on_click=select_home, style=Style(padding="0.5rem 1rem", cursor="pointer")),
        ps.Button("Profile", on_click=select_profile, style=Style(padding="0.5rem 1rem", cursor="pointer")),
        ps.Button("Settings", on_click=select_settings, style=Style(padding="0.5rem 1rem", cursor="pointer")),
        style=Style(
            gap="0.75rem",
            padding="1rem",
            background_color="#eff6ff",
            border="1px dashed #2563eb",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    return ps.Column(
        ps.Heading(
            "PyLage Row — Live Manual",
            style=Style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        ps.Text(
            "Row layout component ke positional alignment aur responsive features test karein:",
            style=Style(color="#64748b", margin_bottom="1.5rem"),
        ),

        ps.Text("1. Basic Horizontal Row (With Gap)", style=Style(font_weight="700", margin_bottom="0.5rem")),
        basic_row,

        ps.Text("2. Justify Content (Space Between)", style=Style(font_weight="700", margin_bottom="0.5rem")),
        justify_row,

        ps.Text("3. Vertical Alignment (Center Aligned)", style=Style(font_weight="700", margin_bottom="0.5rem")),
        align_row,

        ps.Text("4. Flex Wrap Behavior", style=Style(font_weight="700", margin_bottom="0.5rem")),
        wrap_row,

        ps.Text("5. Interactive Nav Row", style=Style(font_weight="700", margin_bottom="0.5rem")),
        ps.Row(
            ps.Text("Active Tab: ", style=Style(font_weight="600")),
            ps.Heading(active_tab, style=Style(color="#2563eb", font_size="1rem")),
            style=Style(gap="0.5rem", margin_bottom="0.5rem", align_items="center"),
        ),
        nav_row,

        style=Style(
            width="100%",
            max_width="750px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )