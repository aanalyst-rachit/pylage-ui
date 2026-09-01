from __future__ import annotations

from pathlib import Path
import time
import webbrowser

from pylage.core.component import Component
from pylage.runtime import Runtime


def run(
    app: Component,
    *,
    title: str = "PyLage App",
    output: str | Path = "index.html",
    serve: bool = False,
    host: str = "127.0.0.1",
    port: int = 0,
    open_browser: bool = True,
) -> Path:
    """
    Render and optionally serve a PyLage application.

    Default behavior remains file-only rendering.

    When serve=True, the local runtime starts and the process
    remains alive until interrupted with Ctrl+C.
    """

    if not isinstance(app, Component):
        raise TypeError(
            "pylage.run() expects a Component as the root app."
        )

    if not serve:
        from pylage.renderers.html import render_document

        document = render_document(
            app,
            title=title,
        )

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            document,
            encoding="utf-8",
        )

        return output_path

    runtime = Runtime(
        app,
        title=title,
        output=output,
        host=host,
        port=port,
    )

    output_path = runtime.render()
    url = runtime.start()

    print(f"PyLage app running at {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:
        webbrowser.open(url)

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nStopping PyLage...")

    finally:
        runtime.stop()

    return output_path
