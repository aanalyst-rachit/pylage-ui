from pathlib import Path
from pylage import (
    Button,
    Card,
    Column,
    Heading,
    Row,
    State,
    Text,
    run,
)
from pylage.core.component import component


def get_nav_interaction_app():
    # -------------------------------------------------------------
    # REACTIVE STATES
    # -------------------------------------------------------------
    active_tab = State("tab1")
    current_page = State(1)
    drawer_open = State(False)
    dialog_open = State(False)
    popover_open = State(False)
    menu_selected = State("Home")

    # -------------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------------
    def set_tab(tab_name):
        return lambda payload=None: active_tab.set(tab_name)

    def change_page(delta):
        def handler(payload=None):
            new_pg = max(1, current_page.get() + delta)
            current_page.set(new_pg)

        return handler

    def toggle_drawer(payload=None):
        drawer_open.set(not drawer_open.get())

    def toggle_dialog(payload=None):
        dialog_open.set(not dialog_open.get())

    def toggle_popover(payload=None):
        popover_open.set(not popover_open.get())

    def select_menu_item(item):
        return lambda payload=None: menu_selected.set(item)

    # -------------------------------------------------------------
    # UI COMPONENTS LAYOUT
    # -------------------------------------------------------------
    return Column(
        Heading("PyLage Navigation & Interaction Components Demo"),
        # 1. NAVIGATION & BREADCRUMBS
        Card(
            Heading("1. Navigation & Breadcrumbs"),
            Row(
                Text("Home"),
                Text(" > "),
                Text("Dashboard"),
                Text(" > "),
                Text("Settings"),
                class_name="breadcrumbs",
            ),
            class_name="demo-card",
        ),
        # 2. TABS COMPONENT
        Card(
            Heading("2. Tabs Component"),
            Row(
                Button("Tab 1", on_click=set_tab("tab1")),
                Button("Tab 2", on_click=set_tab("tab2")),
                Button("Tab 3", on_click=set_tab("tab3")),
            ),
            Text("Active Tab Payload: "),
            Text(active_tab),
            class_name="demo-card",
        ),
        # 3. PAGINATION COMPONENT
        Card(
            Heading("3. Pagination Component"),
            Row(
                Button("Previous", on_click=change_page(-1)),
                Text(" Page "),
                Text(current_page),
                Text(" "),
                Button("Next", on_click=change_page(1)),
            ),
            class_name="demo-card",
        ),
        # 4. MENU COMPONENT
        Card(
            Heading("4. Menu Component"),
            Row(
                Button("Profile", on_click=select_menu_item("Profile")),
                Button("Settings", on_click=select_menu_item("Settings")),
                Button("Logout", on_click=select_menu_item("Logout")),
            ),
            Text("Selected Menu: "),
            Text(menu_selected),
            class_name="demo-card",
        ),
        # 5. DRAWER COMPONENT
        Card(
            Heading("5. Drawer Component"),
            Button("Toggle Drawer", on_click=toggle_drawer),
            Text("Drawer Visible State: "),
            Text(drawer_open),
            class_name="demo-card",
        ),
        # 6. TOOLTIP & POPOVER COMPONENT
        Card(
            Heading("6. Tooltip & Popover Component"),
            Row(
                component(
                    "span",
                    "Hover over me (Tooltip)",
                    title="This is a native tooltip message",
                ),
                Button("Toggle Popover", on_click=toggle_popover),
            ),
            Text("Popover Active: "),
            Text(popover_open),
            class_name="demo-card",
        ),
        # 7. DIALOG / MODAL COMPONENT
        Card(
            Heading("7. Dialog / Modal Component"),
            Button("Open Dialog Modal", on_click=toggle_dialog),
            Text("Dialog Open State: "),
            Text(dialog_open),
            class_name="demo-card",
        ),
        class_name="container",
    )


def get_app():
    return get_nav_interaction_app()