from pylage import Badge, Text
from pylage.core.renderer import render


def test_badge_creates_badge_component():
    badge = Badge()

    assert badge.type == "Badge"


def test_badge_supports_children():
    badge = Badge(
        Text("New"),
    )

    html = render(badge)

    assert "New" in html


def test_badge_supports_props():
    badge = Badge(
        class_name="status-badge",
        title="Status",
    )

    html = render(badge)

    assert 'class="status-badge"' in html
    assert 'title="Status"' in html
