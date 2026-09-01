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
    is_subscribed = ps.State(True)
    volume_level = ps.State(50)
    selected_date = ps.State("2026-09-01")
    submitted_summary = ps.State("Form submit nahi hua abhi.")

    # State Handlers
    def handle_check(val=None):
        is_subscribed.set(not is_subscribed.value)

    def handle_slider(val=None):
        if isinstance(val, dict):
            val = val.get("value", volume_level.value)
        try:
            volume_level.set(int(val))
        except (ValueError, TypeError):
            pass

    def handle_date(val=None):
        if isinstance(val, dict):
            val = val.get("value", selected_date.value)
        selected_date.set(str(val))

    def handle_form_submit(e=None):
        summary = f"Subscribed: {is_subscribed.value} | Volume: {volume_level.value} | Date: {selected_date.value}"
        submitted_summary.set(summary)

    # -------------------------------------------------------------------------
    # Native PyLage Components (Proper Binding Engine)
    # -------------------------------------------------------------------------

    # 1. Checkbox Component
    chk_node = ps.Checkbox(
        checked=is_subscribed,
        on_change=handle_check,
        style=Style(width="18px", height="18px", cursor="pointer"),
    )

    # 2. Slider Component
    slider_node = ps.Slider(
        value=volume_level,
        min=0,
        max=100,
        on_change=handle_slider,
        style=Style(width="100%", cursor="pointer"),
    )

    # 3. DatePicker Component
    date_node = ps.DatePicker(
        value=selected_date,
        on_change=handle_date,
        style=Style(
            width="100%",
            padding="0.5rem",
            border="1px solid #cbd5e1",
            border_radius="0.375rem",
            background_color="#ffffff",
            color="#0f172a",
        ),
    )

    # -------------------------------------------------------------------------
    # UI Layout Assembly
    # -------------------------------------------------------------------------
    return ps.Column(
        ps.Heading(
            "Form Components Test Suite",
            style=Style(
                font_size="1.75rem",
                font_weight="800",
                color="#0f172a",
                margin_bottom="0.25rem",
            ),
        ),
        ps.Text(
            "Testing Checkbox, Slider, DatePicker, and Form Container interactions.",
            style=Style(color="#64748b", font_size="0.9rem", margin_bottom="1.5rem"),
        ),

        # 1. Checkbox Section
        ps.Column(
            ps.Heading("1. Checkbox Test", style=Style(font_size="1.1rem", font_weight="700", color="#334155")),
            ps.Row(
                ps.Text("Checkbox State: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(is_subscribed, style=Style(color="#2563eb", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            ps.Row(
                chk_node,
                ps.Text("Subscribe to email notifications", style=Style(color="#334155", font_size="0.95rem")),
                style=Style(gap="0.75rem", align_items="center"),
            ),
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1.25rem",
                width="100%",
            ),
        ),

        # 2. Slider Section
        ps.Column(
            ps.Heading("2. Slider (Range) Test", style=Style(font_size="1.1rem", font_weight="700", color="#334155")),
            ps.Row(
                ps.Text("Volume Value: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(volume_level, style=Style(color="#059669", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            slider_node,
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1.25rem",
                width="100%",
            ),
        ),

        # 3. DatePicker Section
        ps.Column(
            ps.Heading("3. DatePicker Test", style=Style(font_size="1.1rem", font_weight="700", color="#334155")),
            ps.Row(
                ps.Text("Selected Date: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(selected_date, style=Style(color="#d97706", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            date_node,
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1.25rem",
                width="100%",
            ),
        ),

        # 4. Form Submit Section
        ps.Column(
            ps.Heading("4. Form Submission Test", style=Style(font_weight="700", color="#334155", font_size="1.1rem")),
            ps.Button(
                "Submit Form",
                on_click=handle_form_submit,
                style=Style(
                    background_color="#2563eb",
                    color="#ffffff",
                    padding="0.6rem 1.2rem",
                    border_radius="0.375rem",
                    font_weight="600",
                    cursor="pointer",
                    margin_bottom="1rem",
                ),
            ),
            ps.Row(
                ps.Text("Result: ", style=Style(font_weight="600", color="#475569")),
                ps.Text(submitted_summary, style=Style(color="#0f172a", font_weight="500")),
                style=Style(gap="0.5rem", align_items="center"),
            ),
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                width="100%",
            ),
        ),

        style=Style(
            width="100%",
            max_width="580px",
            padding="2rem",
            background_color="#f8fafc",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )