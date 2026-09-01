from playwright.sync_api import expect, sync_playwright

import pylage as ps
from pylage.core.registry import registry
from pylage.core.renderer import render
from pylage.runtime import Runtime


def test_switch_checked_false_does_not_render_checked():
    switch = ps.Switch(checked=False)

    html = render(switch)

    assert 'type="checkbox"' in html
    assert " checked" not in html


def test_switch_checked_true_renders_checked():
    switch = ps.Switch(checked=True)

    html = render(switch)

    assert 'type="checkbox"' in html
    assert "checked" in html


def test_switch_preserves_props_and_event():
    def changed(payload):
        return payload

    switch = ps.Switch(
        class_name="theme-switch",
        title="Enable dark mode",
        on_change=changed,
    )

    html = render(switch)

    assert 'class="theme-switch"' in html
    assert 'title="Enable dark mode"' in html
    assert "change" in switch.events


def test_switch_checked_state_is_resolved_for_rendering():
    state = ps.State(True)
    switch = ps.Switch(checked=state)

    html = render(switch)

    assert "checked" in html


def test_switch_registry_declares_checked_as_boolean():
    definition = registry.get("Switch")

    assert definition is not None
    assert definition.props is not None
    assert definition.props["checked"].kind == "boolean"
    assert definition.props["checked"].html_name == "checked"


def test_switch_state_update_controls_browser_checked_property():
    enabled = ps.State(False)
    switch = ps.Switch(checked=enabled)

    app = ps.Column(switch)

    runtime = Runtime(
        app,
        title="B3 Switch State Binding",
        output="test_output/b3_switch_state_binding/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            locator = page.locator(
                f'[data-pylage-id="{switch.id}"]'
            )

            expect(locator).not_to_be_checked()

            enabled.set(True)

            expect(locator).to_be_checked()

            browser.close()

    finally:
        runtime.stop()


def test_switch_change_event_reports_checked_state():
    received = []

    def on_change(payload):
        received.append(payload)

    switch = ps.Switch(
        checked=False,
        on_change=on_change,
    )

    app = ps.Column(switch)

    runtime = Runtime(
        app,
        title="B3 Switch Change Event",
        output="test_output/b3_switch_change_event/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            locator = page.locator(
                f'[data-pylage-id="{switch.id}"]'
            )

            locator.check()

            expect(locator).to_be_checked()

            assert received
            assert received[-1]["checked"] is True

            browser.close()

    finally:
        runtime.stop()
