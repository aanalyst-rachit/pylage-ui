import sys
from pathlib import Path

# Ensure local pylage import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps
from pylage import Style

def get_app():
    # 1. Exact Working Pattern: Reactive State
    count = ps.State(0)

    # 2. Exact Working Pattern: Callback function
    def handle_click():
        count.set(count.value + 1)
        return count.value

    # 3. Direct State object bound to Heading
    status = ps.Heading(count)

    # 4. Buttons initialization with exact test-case syntax (on_click=handle_click)
    basic = ps.Button("Basic Button", on_click=handle_click)

    primary = ps.Button(
        "Primary Button",
        on_click=handle_click,
        style=Style(
            background_color="#2563eb",
            color="#ffffff",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    large = ps.Button(
        "Large Button",
        on_click=handle_click,
        style=Style(
            background_color="#7c3aed",
            color="#ffffff",
            padding="1rem 2rem",
            font_size="1.1rem",
            font_weight="700",
            border_radius="0.75rem",
            cursor="pointer",
        ),
    )

    outline = ps.Button(
        "Outline Button",
        on_click=handle_click,
        style=Style(
            background_color="#ffffff",
            color="#2563eb",
            border="1px solid #2563eb",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    danger = ps.Button(
        "Delete",
        on_click=handle_click,
        style=Style(
            background_color="#dc2626",
            color="#ffffff",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    custom = ps.Button(
        "Custom Button",
        on_click=handle_click,
        style=Style(
            background_color="#fef3c7",
            color="#92400e",
            border="2px solid #f59e0b",
            border_radius="999px",
            padding="0.75rem 1.5rem",
            font_weight="700",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
            cursor="pointer",
        ),
    )

    return ps.Column(
        ps.Text(
            "PyLage Button — Live Manual",
            style=Style(
                font_size="1.75rem",
                font_weight="700",
                color="#0f172a",
                margin_bottom="0.5rem",
            ),
        ),
        ps.Text(
            "Button click count test karne ke liye niche buttons par click karo:",
            style=Style(color="#64748b", margin_bottom="1.5rem"),
        ),

        # State output component
        status,

        ps.Text("Basic", style=Style(font_weight="700", margin_bottom="0.5rem")),
        basic,

        ps.Text("Primary", style=Style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        primary,

        ps.Text("Large", style=Style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        large,

        ps.Text("Outline", style=Style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        outline,

        ps.Text("Danger", style=Style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        danger,

        ps.Text("Custom", style=Style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        custom,

        style=Style(
            width="100%",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    )