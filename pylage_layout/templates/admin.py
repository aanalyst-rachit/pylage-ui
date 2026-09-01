"""Admin panel page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import Row, Column, Card, Heading, Text, Button, Badge


def AdminPanel(
    title: Any = "Admin Panel",
    sidebar: Any = None,
    content: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a reusable admin panel page."""

    if sidebar is None:
        sidebar = Column(
            Heading("Navigation"),
            Text("Dashboard"),
            Text("Users"),
            Text("Settings"),
            class_name="admin-sidebar",
        )

    if content is None:
        stats = Row(
            Card(
                Heading("1,250"),
                Text("Users"),
                class_name="admin-stat-card",
            ),
            Card(
                Heading("₹48K"),
                Text("Revenue"),
                class_name="admin-stat-card",
            ),
            Card(
                Heading("320"),
                Text("Orders"),
                class_name="admin-stat-card",
            ),
            class_name="admin-stats",
        )

        main_content = Column(
            Heading(title),
            stats,
            Card(
                Heading("Recent Activity"),
                Text("No recent activity."),
                class_name="admin-activity",
            ),
            Card(
                Heading("Quick Actions"),
                Row(
                    Button("Add User"),
                    Button("View Reports"),
                    Button("Settings"),
                ),
                class_name="admin-actions",
            ),
            class_name="admin-main",
        )
    else:
        main_content = content

    body = Row(
        sidebar,
        main_content,
        class_name="admin-body",
    )

    children = [body]

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(*children, **props)
    )
