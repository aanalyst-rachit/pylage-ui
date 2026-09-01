from pathlib import Path
from pylage import (
    Card,
    Column,
    Heading,
    RadioGroup,
    Row,
    Select,
    State,
    Switch,
    Text,
)
from pylage.core.component import component


def Option(label: str, value: str, **props):
    """Helper component for Select dropdown options."""
    return component("option", label, value=value, **props)


def RadioInput(name: str, value: str, checked: bool = False, on_change=None):
    """Helper component to avoid keyword collision on 'type' argument."""
    return component(
        "input",
        name=name,
        value=value,
        checked=checked,
        on_change=on_change,
        props={"type": "radio"},
    )


def get_app():
    # -------------------------------------------------------------
    # REACTIVE STATES
    # -------------------------------------------------------------
    selected_theme = State("Dark Mode")
    switch_active = State(True)
    selected_framework = State("PyLage")

    # -------------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------------
    def on_radio_change(payload=None):
        if isinstance(payload, dict) and "value" in payload:
            selected_theme.set(payload["value"])
        elif isinstance(payload, str):
            selected_theme.set(payload)

    def on_switch_toggle(payload=None):
        if isinstance(payload, dict) and "checked" in payload:
            switch_active.set(payload["checked"])
        else:
            switch_active.set(not switch_active.get())

    def on_select_change(payload=None):
        if isinstance(payload, dict) and "value" in payload:
            selected_framework.set(payload["value"])
        elif isinstance(payload, str):
            selected_framework.set(payload)

    # -------------------------------------------------------------
    # UI COMPONENTS LAYOUT
    # -------------------------------------------------------------
    return Column(
        Heading("PyLage Components Working Live Demo"),
        # 1. RADIO BUTTON GROUP DEMO
        Card(
            Heading("1. Radio Group Component"),
            RadioGroup(
                Row(
                    RadioInput(
                        name="theme_group",
                        value="Light Mode",
                        on_change=on_radio_change,
                    ),
                    Text("Light Mode"),
                ),
                Row(
                    RadioInput(
                        name="theme_group",
                        value="Dark Mode",
                        checked=True,
                        on_change=on_radio_change,
                    ),
                    Text("Dark Mode"),
                ),
                Row(
                    RadioInput(
                        name="theme_group",
                        value="System Default",
                        on_change=on_radio_change,
                    ),
                    Text("System Default"),
                ),
            ),
            Text("Selected Theme: "),
            Text(selected_theme),
            class_name="demo-card",
        ),
        # 2. SWITCH COMPONENT DEMO
        Card(
            Heading("2. Switch Component"),
            Row(
                Switch(
                    checked=switch_active,
                    on_change=on_switch_toggle,
                    title="Toggle Status",
                ),
                Text("Toggle Switch State"),
            ),
            Text("Switch Active Status: "),
            Text(switch_active),
            class_name="demo-card",
        ),
        # 3. SELECT COMPONENT DEMO
        Card(
            Heading("3. Select Component"),
            Select(
                Option("PyLage UI Framework", "PyLage"),
                Option("React Web Engine", "React"),
                Option("VueJS Framework", "Vue"),
                value=selected_framework,
                on_change=on_select_change,
            ),
            Text("Selected Option: "),
            Text(selected_framework),
            class_name="demo-card",
        ),
        class_name="container",
    )