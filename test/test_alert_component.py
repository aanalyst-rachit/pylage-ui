from pylage import Alert, Text, Button
from pylage.core.renderer import render


def test_alert_renders_as_div():
    alert = Alert()

    html = render(alert)

    assert "<div" in html


def test_alert_supports_props():
    alert = Alert(
        class_name="warning",
        title="Warning",
    )

    html = render(alert)

    assert 'class="warning"' in html
    assert 'title="Warning"' in html


def test_alert_supports_text():
    alert = Alert(
        text="Something went wrong",
    )

    html = render(alert)

    assert "Something went wrong" in html
