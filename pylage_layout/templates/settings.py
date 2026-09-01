"""Settings page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import (
    Button,
    Card,
    Checkbox,
    Column,
    Form,
    Heading,
    Input,
    Row,
    Select,
    Switch,
    Tabs,
    Text,
)


def SettingsPage(
    account: Any = None,
    preferences: Any = None,
    security: Any = None,
    notifications: Any = None,
    **props: Any,
):
    """Compose a complete settings page from PyLage components."""

    children = []

    if account is None:
        account = Card(
            Heading("Account"),
            Form(
                Input(
                    value="",
                    class_name="settings-name",
                    title="Name",
                ),
                Input(
                    value="",
                    class_name="settings-email",
                    title="Email",
                ),
                Button(
                    "Save Changes",
                    class_name="settings-save",
                ),
                class_name="settings-form",
            ),
            class_name="settings-card",
        )

    if preferences is None:
        preferences = Card(
            Heading("Preferences"),
            Select(
                class_name="settings-theme",
                title="Theme",
            ),
            Switch(
                class_name="settings-auto-save",
                title="Auto Save",
            ),
            class_name="settings-card",
        )

    if security is None:
        security = Card(
            Heading("Security"),
            Input(
                value="",
                class_name="settings-password",
                title="Current Password",
            ),
            Button(
                "Change Password",
                class_name="settings-security-action",
            ),
            class_name="settings-card",
        )

    if notifications is None:
        notifications = Card(
            Heading("Notifications"),
            Checkbox(
                class_name="settings-email-notifications",
                title="Email Notifications",
            ),
            Checkbox(
                class_name="settings-push-notifications",
                title="Push Notifications",
            ),
            class_name="settings-card",
        )

    children.extend(
        [
            Heading("Settings"),
            Text(
                "Manage your account, preferences, security, and notifications."
            ),
            Tabs(
                Text("Account"),
                Text("Preferences"),
                Text("Security"),
                Text("Notifications"),
                class_name="settings-tabs",
            ),
            Row(
                Column(account, class_name="settings-account"),
                Column(preferences, class_name="settings-preferences"),
                class_name="settings-row",
            ),
            Row(
                Column(security, class_name="settings-security"),
                Column(notifications, class_name="settings-notifications"),
                class_name="settings-row",
            ),
        ]
    )

    return Container(
        Stack(
            *children,
            **props,
        )
    )


Settings = SettingsPage
