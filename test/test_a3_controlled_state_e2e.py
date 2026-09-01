from playwright.sync_api import sync_playwright, expect

import pylage as ps
from pylage.runtime import Runtime


def test_controlled_input_survives_bidirectional_updates():
    name = ps.State("Dollar")

    heading = ps.Heading(name)
    input_box = ps.Input(value=name)

    app = ps.Column(
        heading,
        input_box,
    )

    runtime = Runtime(
        app,
        title="A3 Controlled State E2E",
        output="test_output/a3_controlled_state_e2e/index.html",
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

            # Initial controlled value.
            expect(heading_locator).to_have_text("Dollar")
            expect(input_locator).to_have_value("Dollar")

            # Browser → Python State.
            input_locator.fill("Racit")

            expect(heading_locator).to_have_text("Racit")
            expect(input_locator).to_have_value("Racit")
            assert name.value == "Racit"

            # Python State → Browser.
            name.set("PyLage")

            expect(heading_locator).to_have_text("PyLage")
            expect(input_locator).to_have_value("PyLage")
            assert name.value == "PyLage"

            browser.close()

    finally:
        runtime.stop()
