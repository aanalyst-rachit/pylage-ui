import pytest
from playwright.sync_api import sync_playwright, expect

import pylage as ps
from pylage.runtime import Runtime


def test_browser_reactive_counter():
    print("=== PYLAGE BROWSER REACTIVE COUNTER TEST ===")

    count = ps.State(0)

    def increment():
        count.set(count.value + 1)
        return count.value

    heading = ps.Heading(count)

    button = ps.Button(
        "Increment",
        on_click=increment,
    )

    app = ps.Column(
        heading,
        button,
    )

    runtime = Runtime(
        app,
        title="PyLage Reactive Counter",
        output="test_output/browser_reactive_counter/index.html",
    )

    try:
        url = runtime.start()

        print("HTTP:", url)
        print("WebSocket:", runtime._websocket.url)
        print("Heading ID:", heading.id)
        print("Button ID:", button.id)
        print("Initial state:", count.value)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            heading_locator = page.locator(
                f'[data-pylage-id="{heading.id}"]'
            )

            button_locator = page.locator(
                f'[data-pylage-id="{button.id}"]'
            )

            expect(heading_locator).to_have_text("0")
            expect(button_locator).to_have_text("Increment")

            print("Browser loaded: PASS")
            print("Initial state: 0")

            button_locator.click()
            expect(heading_locator).to_have_text("1")
            assert count.value == 1
            print("Click 1: Python State = 1")

            button_locator.click()
            expect(heading_locator).to_have_text("2")
            assert count.value == 2
            print("Click 2: Python State = 2")

            button_locator.click()
            expect(heading_locator).to_have_text("3")
            assert count.value == 3
            print("Click 3: Python State = 3")

            browser.close()

        print()
        print("Browser → WebSocket event: PASS")
        print("WebSocket → Python callback: PASS")
        print("Python callback → State.set(): PASS")
        print("State → Browser DOM: PASS")
        print("State value sequence 1 → 2 → 3: PASS")
        print()
        print("=== BROWSER REACTIVE COUNTER PASS ===")

    finally:
        runtime.stop()
        print("Runtime stopped.")
