from playwright.sync_api import sync_playwright, expect

import pylage as ps
from pylage.runtime import Runtime


def test_python_state_update_controls_browser_input():
    name = ps.State("Dollar")

    heading = ps.Heading(name)
    input_box = ps.Input(value=name)

    app = ps.Column(
        heading,
        input_box,
    )

    runtime = Runtime(
        app,
        title="A3 Controlled State Binding",
        output="test_output/a3_controlled_state_binding/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            heading_locator = page.locator(
                f'[data-pylage-id="{heading.id}"]'
            )
            input_locator = page.locator(
                f'[data-pylage-id="{input_box.id}"]'
            )

            expect(heading_locator).to_have_text("Dollar")
            expect(input_locator).to_have_value("Dollar")

            # Python → State → WebSocket → Browser DOM
            name.set("Racit")

            expect(heading_locator).to_have_text("Racit")
            expect(input_locator).to_have_value("Racit")

            browser.close()

    finally:
        runtime.stop()
