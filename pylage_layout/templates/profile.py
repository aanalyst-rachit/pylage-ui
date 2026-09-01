"""Profile page template for PyLage Layout."""

from typing import Any

from ..layouts import Container, Stack
from pylage.components import (
    Avatar,
    Button,
    Card,
    Column,
    Heading,
    Row,
    Text,
)


def ProfilePage(
    name: Any = "Rachit",
    role: Any = "Developer",
    email: Any = "user@example.com",
    phone: Any = "",
    location: Any = "",
    avatar: Any = "/avatar.png",
    actions: Any = None,
    content: Any = None,
    **props: Any,
):
    """Compose a reusable profile page from existing PyLage components."""

    profile_header = Row(
        Avatar(
            class_name="profile-avatar",
        ),
        Column(
            Heading(name),
            Text(role),
            class_name="profile-identity",
        ),
        class_name="profile-header",
    )

    profile_info = Card(
        Heading("Profile Information"),
        Text(f"Email: {email}"),
        Text(f"Phone: {phone}"),
        Text(f"Location: {location}"),
        class_name="profile-info",
    )

    if actions is None:
        actions = Row(
            Button(
                "Edit Profile",
                class_name="profile-edit",
            ),
            Button(
                "Change Password",
                class_name="profile-password",
            ),
            class_name="profile-actions",
        )

    children = [
        profile_header,
        profile_info,
        actions,
    ]

    if content is not None:
        children.append(content)

    return Container(
        Stack(
            *children,
            **props,
        )
    )
