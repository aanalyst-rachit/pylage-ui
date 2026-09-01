from pylage import Dialog, Text, Button
from pylage.core.renderer import render


def test_dialog_renders_as_dialog():
    dialog = Dialog()

    html = render(dialog)

    assert "<dialog" in html
    assert "</dialog>" in html


def test_dialog_renders_children():
    dialog = Dialog(
        Text("Hello Dialog"),
        Button("Close"),
    )

    html = render(dialog)

    assert "Hello Dialog" in html
    assert "Close" in html


def test_dialog_supports_props():
    dialog = Dialog(
        class_name="app-dialog",
        title="Confirmation",
    )

    html = render(dialog)

    assert 'class="app-dialog"' in html
    assert 'title="Confirmation"' in html
