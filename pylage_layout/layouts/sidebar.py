"""Sidebar layout primitive for PyLage Layout."""

from typing import Any

from pylage.components import Column, Row


def SidebarLayout(
    sidebar: Any,
    content: Any,
    *,
    class_name: str = "sidebar-layout",
    sidebar_width: str = "260px",
    gap: str = "1rem",
    **props: Any,
):
    sidebar_style = {
        "width": sidebar_width,
        "flex_shrink": "0",
    }

    content_style = {
        "width": "100%",
        "min_width": "0",
        "flex": "1",
    }

    sidebar_component = Column(
        sidebar,
        style=sidebar_style,
    )

    content_component = Column(
        content,
        style=content_style,
    )

    return Row(
        sidebar_component,
        content_component,
        class_name=class_name,
        style={
            "width": "100%",
            "display": "flex",
            "flex_direction": "row",
            "gap": gap,
        },
        **props,
    )
