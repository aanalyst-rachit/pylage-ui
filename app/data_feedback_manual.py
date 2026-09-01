
from pylage.core.component import Component
from pylage import State, Style
from pylage.components import (
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
    Table,
    Text,
    Toast,
)

def get_app() -> Component:
    # --- Reactive States ---
    toast_visible = State(True)
    progress_val = State(45)

    def close_toast():
        toast_visible.value = False

    def boost_progress():
        if progress_val.value >= 100:
            progress_val.value = 10
        else:
            progress_val.value += 15

    # --- UI Layout ---
    app = Column(style=Style(padding="24px", gap="24px", max_width="900px", margin="0 auto"))
    
    # Header
    app.add(
        Heading("📊 Data & Feedback Components Live Demo", level=2),
        Text("Interactive showcase for testing component visual output and state integration.")
    )

    # 1. Table Component
    app.add(
        Card(
            Heading("1. Table Component", level=3),
            Table(
                headers=["ID", "User", "Role", "Status"],
                rows=[
                    ["101", "Rachit", "Admin", "Active"],
                    ["102", "Alex", "Developer", "Pending"],
                    ["103", "Sarah", "Designer", "Active"],
                ],
                style=Style(margin_top="12px", width="100%")
            )
        )
    )

    # 2. Alert Component
    app.add(
        Card(
            Heading("2. Alert Component", level=3),
            Column(
                Alert("Success! Your changes have been saved cleanly.", variant="success"),
                Alert("Warning: Low disk space remaining on server.", variant="warning"),
                Alert("Error: Failed to connect to local WebSocket.", variant="error"),
                style=Style(gap="8px", margin_top="12px")
            )
        )
    )

    # 3. Toast Component
    app.add(
        Card(
            Heading("3. Toast Component", level=3),
            Column(
                Toast(
                    "Notification: State update broadcast successfully!",
                    visible=toast_visible,
                    on_close=close_toast
                ),
                Button("Dismiss / Toggle Toast State", on_click=close_toast, style=Style(margin_top="8px"))
            )
        )
    )

    # 4. Spinner Component
    app.add(
        Card(
            Heading("4. Spinner Component", level=3),
            Row(
                Spinner(size="sm"),
                Spinner(size="md"),
                Spinner(size="lg"),
                style=Style(gap="16px", align_items="center", margin_top="12px")
            )
        )
    )

    # 5. ProgressBar Component
    app.add(
        Card(
            Heading("5. ProgressBar Component", level=3),
            Column(
                ProgressBar(value=progress_val, max=100),
                Button("Boost Progress State (+15%)", on_click=boost_progress, style=Style(margin_top="8px"))
            )
        )
    )

    # 6. Skeleton Component
    app.add(
        Card(
            Heading("6. Skeleton Component", level=3),
            Column(
                Skeleton(height="20px", width="60%"),
                Skeleton(height="14px", width="100%"),
                Skeleton(height="14px", width="85%"),
                style=Style(gap="8px", margin_top="12px")
            )
        )
    )

    # 7. Badge Component
    app.add(
        Card(
            Heading("7. Badge Component", level=3),
            Row(
                Badge("New", variant="primary"),
                Badge("Completed", variant="success"),
                Badge("In Progress", variant="warning"),
                Badge("Deprecated", variant="danger"),
                style=Style(gap="8px", margin_top="12px")
            )
        )
    )

    # 8. Accordion Component
    app.add(
        Card(
            Heading("8. Accordion Component", level=3),
            Accordion(
                items=[
                    {"title": "Section 1: Architecture Overview", "content": "PyLage utilizes WebSocket reactive tree patching."},
                    {"title": "Section 2: State Management", "content": "State binding maps dependencies directly to DOM attributes."},
                ],
                style=Style(margin_top="12px")
            )
        )
    )

    # 9. Carousel Component
    app.add(
        Card(
            Heading("9. Carousel Component", level=3),
            Carousel(
                items=[
                    Card(Text("Slide 1: Real-time UI Engine")),
                    Card(Text("Slide 2: Reactive WebSockets")),
                    Card(Text("Slide 3: High Performance Diffing")),
                ],
                style=Style(margin_top="12px")
            )
        )
    )

    return app