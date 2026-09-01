from playwright.sync_api import sync_playwright

import pylage as ps
from pylage.runtime import Runtime


def test_browser_event_payload_protocol():
    received = {
        "input": None,
        "checkbox": None,
        "select": None,
        "multi": None,
    }

    def on_input(payload):
        received["input"] = payload

    def on_checkbox(payload):
        received["checkbox"] = payload

    def on_select(payload):
        received["select"] = payload

    def on_multi(payload):
        received["multi"] = payload

    input_box = ps.Input(
        "",
        on_input=on_input,
    )

    checkbox = ps.Checkbox(
        on_change=on_checkbox,
    )

    select = ps.Select(
        ps.Option("India", value="india"),
        ps.Option("Japan", value="japan"),
        on_change=on_select,
    )

    multi_select = ps.Select(
        ps.Option(
            "Python",
            value="python",
        ),
        ps.Option(
            "Rust",
            value="rust",
        ),
        ps.Option(
            "Go",
            value="go",
        ),
        multiple=True,
        on_change=on_multi,
    )

    app = ps.Column(
        input_box,
        checkbox,
        select,
        multi_select,
    )

    runtime = Runtime(
        app,
        title="PyLage A2 Event Payload Protocol",
        output=(
            "test_output/"
            "browser_event_payload_protocol/"
            "index.html"
        ),
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
            )
            page = browser.new_page()

            page.goto(url)

            input_locator = page.locator(
                f'[data-pylage-id="{input_box.id}"]'
            )

            checkbox_locator = page.locator(
                f'[data-pylage-id="{checkbox.id}"]'
            )

            select_locator = page.locator(
                f'[data-pylage-id="{select.id}"]'
            )

            multi_locator = page.locator(
                f'[data-pylage-id="{multi_select.id}"]'
            )

            input_locator.fill("Dollar")

            checkbox_locator.check()

            select_locator.select_option(
                "japan",
            )

            multi_locator.select_option(
                ["python", "go"],
            )

            for _ in range(50):
                if all(
                    value is not None
                    for value in received.values()
                ):
                    break

                page.wait_for_timeout(100)

            assert received["input"] == {
                "value": "Dollar",
                "checked": False,
            }

            assert received["checkbox"] == {
                "value": "on",
                "checked": True,
            }

            assert received["select"] == {
                "value": "japan",
                "selectedIndex": 1,
            }

            assert received["multi"]["value"] == "python"
            assert received["multi"]["selectedIndex"] == 0
            assert received["multi"]["selectedOptions"] == [
                {
                    "value": "python",
                    "text": "Python",
                },
                {
                    "value": "go",
                    "text": "Go",
                },
            ]

            browser.close()

    finally:
        runtime.stop()
