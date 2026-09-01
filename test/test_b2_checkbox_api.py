import pylage as ps
from pylage.core.renderer import render


def test_checkbox_checked_false_does_not_render_checked():
    checkbox = ps.Checkbox(checked=False)

    html = render(checkbox)

    assert 'type="checkbox"' in html
    assert " checked" not in html


def test_checkbox_checked_true_renders_checked():
    checkbox = ps.Checkbox(checked=True)

    html = render(checkbox)

    assert 'type="checkbox"' in html
    assert " checked" in html


def test_checkbox_preserves_existing_props_and_event():
    received = []

    checkbox = ps.Checkbox(
        class_name="agree",
        title="Accept terms",
        checked=True,
        on_change=lambda payload: received.append(payload),
    )

    html = render(checkbox)

    assert 'class="agree"' in html
    assert 'title="Accept terms"' in html
    assert " checked" in html
    assert "data-pylage-events=\"change\"" in html


def test_checkbox_checked_state_is_resolved_for_rendering():
    checked = ps.State(False)

    checkbox = ps.Checkbox(checked=checked)

    html = render(checkbox)

    assert 'type="checkbox"' in html
    assert " checked" not in html

    checked.set(True)

    html = render(checkbox)

    assert " checked" in html


def test_checkbox_registry_declares_checked_as_boolean():
    from pylage.core.registry import registry

    definition = registry.get("Checkbox")

    assert definition is not None
    assert definition.props is not None
    assert "checked" in definition.props
    assert definition.props["checked"].kind == "boolean"
    assert definition.props["checked"].html_name == "checked"


def test_checkbox_state_update_controls_browser_checked_property():
    from playwright.sync_api import sync_playwright, expect
    from pylage.runtime import Runtime

    checked = ps.State(False)
    checkbox = ps.Checkbox(checked=checked)

    runtime = Runtime(
        checkbox,
        title="B2 Checkbox State Binding",
        output="test_output/b2_checkbox_state_binding/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            locator = page.locator(
                f'[data-pylage-id="{checkbox.id}"]'
            )

            expect(locator).not_to_be_checked()

            # Python → State → WebSocket → Browser DOM
            checked.set(True)

            expect(locator).to_be_checked()

            checked.set(False)

            expect(locator).not_to_be_checked()

            browser.close()

    finally:
        runtime.stop()
