from pylage import Form, Input, Button
from pylage.core.renderer import render


def test_form_renders_as_form():
    form = Form(
        Input(),
        Button("Submit"),
    )

    html = render(form)

    assert "<form" in html
    assert "</form>" in html


def test_form_renders_children():
    form = Form(
        Input(),
        Button("Submit"),
    )

    html = render(form)

    assert "<input" in html
    assert "<button" in html
    assert "Submit" in html


def test_form_supports_props():
    form = Form(
        method="post",
        action="/submit",
    )

    html = render(form)

    assert 'method="post"' in html
    assert 'action="/submit"' in html


def test_form_supports_submit_event():
    form = Form(on_submit=lambda payload: None)

    html = render(form)

    assert 'data-pylage-events="submit"' in html


def test_form_submit_event_is_in_client_runtime():
    from pylage.runtime.client import CLIENT_RUNTIME

    assert 'document.addEventListener("submit", handleEvent)' in CLIENT_RUNTIME
    assert "event.preventDefault()" in CLIENT_RUNTIME


def test_form_submit_runtime_builds_payload():
    from pylage.runtime.client import CLIENT_RUNTIME

    assert "FormData" in CLIENT_RUNTIME
    assert "sendEvent(componentId, event.type, payload)" in CLIENT_RUNTIME


def test_form_submit_dispatches_payload():
    from pylage.core.events import EventDispatcher

    received = []

    def handle_submit(payload):
        received.append(payload)
        return "submitted"

    form = Form(
        Input(name="email", value="test@example.com"),
        on_submit=handle_submit,
    )

    dispatcher = EventDispatcher(form)

    result = dispatcher.dispatch(
        form.id,
        "submit",
        {
            "values": {
                "email": "test@example.com",
            }
        },
    )

    assert result == "submitted"
    assert received == [
        {
            "values": {
                "email": "test@example.com",
            }
        }
    ]
