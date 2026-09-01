from pylage import Avatar, Text
from pylage.core.renderer import render


def test_avatar_creates_avatar_component():
    avatar = Avatar()

    assert avatar.type == "Avatar"


def test_avatar_supports_children():
    avatar = Avatar(
        Text("RC"),
    )

    html = render(avatar)

    assert "RC" in html


def test_avatar_supports_props():
    avatar = Avatar(
        class_name="user-avatar",
        title="Rachit",
    )

    html = render(avatar)

    assert 'class="user-avatar"' in html
    assert 'title="Rachit"' in html
