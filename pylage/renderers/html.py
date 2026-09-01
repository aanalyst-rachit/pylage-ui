from __future__ import annotations

from html import escape

from pylage.core.component import Component
from pylage.core.renderer import render
from pylage.runtime.client import get_client_runtime


class HTMLDocumentRenderer:
    """Build a complete standalone HTML document."""

    def render(
        self,
        component: Component,
        title: str = "PyLage App",
        websocket_url: str | None = None,
    ) -> str:
        body = render(component)
        runtime = get_client_runtime(websocket_url)

        safe_title = escape(title)

        # get_client_runtime() contains:
        #   1. bootstrap <script>
        #   2. raw client JavaScript
        #
        # Split them so the raw JavaScript is also placed
        # inside a real <script> tag.
        if "</script>" in runtime:
            bootstrap, client_runtime = runtime.split(
                "</script>",
                1,
            )

            bootstrap += "</script>"

            client_runtime = client_runtime.strip()

            if client_runtime.startswith("<script>"):
                client_runtime = client_runtime[len("<script>"):]

            if client_runtime.endswith("</script>"):
                client_runtime = client_runtime[:-len("</script>")]

            scripts = (
                bootstrap
                + "\n<script>\n"
                + client_runtime.strip()
                + "\n</script>"
            )
        else:
            scripts = (
                "<script>\n"
                + runtime
                + "\n</script>"
            )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
</head>
<body>
{body}
{scripts}
</body>
</html>
"""


def render_document(
    component: Component,
    title: str = "PyLage App",
    websocket_url: str | None = None,
) -> str:
    return HTMLDocumentRenderer().render(
        component,
        title=title,
        websocket_url=websocket_url,
    )