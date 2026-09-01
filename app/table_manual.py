# app/data_feedback_manual.py

from pylage import (
    Accordion,
    Alert,
    Badge,
    Button,
    Card,
    Carousel,
    Column,
    Heading,
    ProgressBar,
    Row,
    Skeleton,
    Spinner,
    State,
    Style,
    Table,
    Text,
    Toast,
)
from pylage.core.component import Component, component


def get_app() -> Component:
    # State management for interactive demos
    progress = State(45)
    toast_visible = State(True)
    accordion_open = State("section1")
    carousel_index = State(0)

    def increase_progress():
        val = progress.value + 15
        progress.value = 100 if val > 100 else val

    def reset_progress():
        progress.value = 0

    def toggle_toast():
        toast_visible.value = not toast_visible.value

    return component(
        "div",
        Style(padding="20px", gap="20px", display="flex", flex_direction="column"),
        Heading("📊 Data & Feedback Components Live Demo", level=1),
        # 1. Badge & Alert
        Card(
            Heading("1. Badge & Alert", level=3),
            Row(
                Badge("Active Status", variant="success"),
                Badge("Warning", variant="warning"),
                Badge("Error", variant="danger"),
                Style(gap="10px", margin_bottom="15px"),
            ),
            Alert(
                "Info Alert: System maintenance scheduled for tonight.",
                type="info",
            ),
            Alert("Success Alert: Operation completed successfully!", type="success"),
        ),
        # 2. Table
        Card(
            Heading("2. Table Component", level=3),
            Table(
                headers=["ID", "Name", "Role", "Status"],
                data=[
                    ["1", "Rahul Sharma", "Developer", "Active"],
                    ["2", "Priya Singh", "Designer", "Pending"],
                    ["3", "Amit Kumar", "Manager", "Active"],
                ],
            ),
        ),
        # 3. Toast
        Card(
            Heading("3. Toast Component", level=3),
            Button(
                "Toggle Toast View",
                on_click=toggle_toast,
            ),
            Toast(
                "New Notification: You received a message!",
                visible=toast_visible,
            ),
        ),
        # 4. Spinner, ProgressBar & Skeleton
        Card(
            Heading("4. Loading States (Spinner, ProgressBar, Skeleton)", level=3),
            Row(
                Text("Spinner Loading: "),
                Spinner(size="medium"),
                Style(align_items="center", gap="10px"),
            ),
            Row(
                Button("Increase Progress", on_click=increase_progress),
                Button("Reset", on_click=reset_progress),
                Style(gap="10px", margin_top="10px", margin_bottom="10px"),
            ),
            ProgressBar(value=progress, max=100),
            Heading("Skeleton Placeholder Loading:", level=4),
            Skeleton(width="100%", height="20px"),
            Skeleton(width="60%", height="20px"),
        ),
        # 5. Accordion
        Card(
            Heading("5. Accordion Component", level=3),
            Accordion(
                items=[
                    {
                        "id": "section1",
                        "title": "Section 1: Details",
                        "content": "Content for section 1 is loaded here.",
                    },
                    {
                        "id": "section2",
                        "title": "Section 2: Additional Info",
                        "content": "Additional information for section 2.",
                    },
                ],
                active_id=accordion_open,
            ),
        ),
        # 6. Carousel
        Card(
            Heading("6. Carousel Component", level=3),
            Carousel(
                items=[
                    "Slide 1: Welcome to PyLage Showcase",
                    "Slide 2: High Performance Python UI Framework",
                    "Slide 3: Reactive State and Modern Component System",
                ],
                current_index=carousel_index,
            ),
        ),
    )