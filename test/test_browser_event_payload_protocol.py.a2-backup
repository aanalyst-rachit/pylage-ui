from playwright.sync_api import sync_playwright, expect

import pylage as ps
from pylage.runtime import Runtime


def test_browser_input_binding():
    print("=== PYLAGE BROWSER INPUT BINDING TEST ===")

    name = ps.State("Dollar")

    heading = ps.Heading(name)

    input_box = ps.Input(
        value=name,
    )

    app = ps.Column(
        heading,
        input_box,
    )

    runtime = Runtime(
        app,
        title="PyLage Input Binding",
        output="test_output/browser_input_binding/index.html",
    )

    try:
        url = runtime.start()

        print("HTTP:", url)
        print("WebSocket:", runtime._websocket.url)
        print("Heading ID:", heading.id)
        print("Input ID:", input_box.id)
        print("Initial state:", name.value)

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

            print("Browser loaded: PASS")
            print("Initial state: Dollar")

            input_locator.fill("Racit")

            expect(heading_locator).to_have_text("Racit")
            expect(input_locator).to_have_value("Racit")

            assert name.value == "Racit"

            print("Browser input: PASS")
            print("Browser → WebSocket: PASS")
            print("WebSocket → Python State: PASS")
            print("State → Browser DOM: PASS")
            print("Final state:", name.value)

            browser.close()

        print()
        print("=== BROWSER INPUT BINDING PASS ===")

    finally:
        runtime.stop()
        print("Runtime stopped.")
