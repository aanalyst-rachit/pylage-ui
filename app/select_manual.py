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
    selected_language = ps.State("Python")
    selected_database = ps.State("postgresql")

    # State Handlers
    def handle_language_change(val):
        clean_val = val.get("value", val) if isinstance(val, dict) else str(val)
        selected_language.set(clean_val)

    def handle_database_change(val):
        clean_val = val.get("value", val) if isinstance(val, dict) else str(val)
        selected_database.set(clean_val)

    # -------------------------------------------------------------------------
    # Native PyLage Select Generator
    # -------------------------------------------------------------------------
    def build_select(options_list, current_state, on_change_fn):
        # 1. Agar PyLage me native Select component hai
        if hasattr(ps, "Select"):
            try:
                return ps.Select(
                    options=options_list,
                    value=current_state.value,
                    on_change=on_change_fn,
                    style=Style(
                        width="100%",
                        padding="0.6rem",
                        border="1px solid #cbd5e1",
                        border_radius="0.375rem",
                        background_color="#ffffff",
                        color="#0f172a",
                        font_size="0.95rem",
                        cursor="pointer",
                    ),
                )
            except Exception:
                pass

        # 2. Native Component Builder with raw HTML props
        from pylage.core.component import Component

        select_node = Component("select")
        select_node.props["value"] = current_state.value
        select_node.on("change", on_change_fn)

        # Style dict injection directly inside props
        select_node.props["style"] = {
            "width": "100%",
            "padding": "0.6rem",
            "border": "1px solid #cbd5e1",
            "borderRadius": "0.375rem",
            "backgroundColor": "#ffffff",
            "color": "#0f172a",
            "fontSize": "0.95rem",
            "cursor": "pointer",
        }

        # Build options
        for opt in options_list:
            val = opt.get("value") if isinstance(opt, dict) else opt
            lbl = opt.get("label") if isinstance(opt, dict) else opt

            opt_node = Component("option")
            opt_node.props["value"] = str(val)
            opt_node.children = [str(lbl)]

            if str(val) == str(current_state.value):
                opt_node.props["selected"] = True

            select_node.children.append(opt_node)

        return select_node

    # -------------------------------------------------------------------------
    # UI Layout
    # -------------------------------------------------------------------------
    return ps.Column(
        ps.Heading(
            "Select (Dropdown) Component Demo",
            style=Style(
                font_size="1.75rem",
                font_weight="800",
                color="#0f172a",
                margin_bottom="0.25rem",
            ),
        ),
        ps.Text(
            "Interactive demonstration of single-select dropdown state in PyLage.",
            style=Style(color="#64748b", font_size="0.9rem", margin_bottom="1.5rem"),
        ),

        # DEMO 1: Simple Options
        ps.Column(
            ps.Row(
                ps.Text("Selected Language: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(selected_language, style=Style(color="#2563eb", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            build_select(
                options_list=["Python", "JavaScript", "Rust", "Go", "C++"],
                current_state=selected_language,
                on_change_fn=handle_language_change,
            ),
            style=Style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1.5rem",
                width="100%",
            ),
        ),

        # DEMO 2: Key-Value Options
        ps.Column(
            ps.Row(
                ps.Text("Selected Database: ", style=Style(font_weight="500", color="#475569")),
                ps.Text(selected_database, style=Style(color="#059669", font_weight="700")),
                style=Style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            build_select(
                options_list=[
                    {"label": "PostgreSQL (Relational)", "value": "postgresql"},
                    {"label": "MongoDB (NoSQL Document)", "value": "mongodb"},
                    {"label": "Redis (In-Memory Data Store)", "value": "redis"},
                    {"label": "SQLite (Embedded DB)", "value": "sqlite"},
                ],
                current_state=selected_database,
                on_change_fn=handle_database_change,
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
            max_width="560px",
            padding="2rem",
            background_color="#f8fafc",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )