from __future__ import annotations

from pathlib import Path

from pylage.core.component import Component
from pylage.renderers.html import render_document

from pylage.runtime.server import LocalServer
from pylage.runtime.websocket import WebSocketServer


class Runtime:
    """Coordinates PyLage rendering and the local HTTP runtime."""

    def __init__(
        self,
        app: Component,
        *,
        title: str = "PyLage App",
        output: str | Path = "index.html",
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> None:
        if not isinstance(app, Component):
            raise TypeError(
                "Runtime expects a Component as the root app."
            )

        self.app = app
        self.title = title
        self.output = Path(output)
        self.host = host
        self.port = port

        self._server: LocalServer | None = None
        self._websocket: WebSocketServer | None = None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("Runtime is not running.")

        return self._server.url

    @property
    def running(self) -> bool:
        return self._server is not None

    def render(self) -> Path:
        """Render the current app into an HTML document."""

        websocket_url = None
        if self._websocket is not None:
            websocket_url = self._websocket.url

        document = render_document(
            self.app,
            title=self.title,
            websocket_url=websocket_url,
        )

        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(
            document,
            encoding="utf-8",
        )

        return self.output

    def start(self) -> str:
        """Render the app and start the local HTTP server."""

        if self._server is not None:
            raise RuntimeError("Runtime is already running.")

        self._websocket = WebSocketServer(
            self.app,
            host=self.host,
            port=0,
        )

        try:
            websocket_url = self._websocket.start()

            document = render_document(
                self.app,
                title=self.title,
                websocket_url=websocket_url,
            )

            output_path = self.output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                document,
                encoding="utf-8",
            )

            self._server = LocalServer(
                output_path.parent,
                host=self.host,
                port=self.port,
                filename=output_path.name,
            )

            return self._server.start()

        except Exception:
            if self._websocket is not None:
                self._websocket.stop()
                self._websocket = None

            self._server = None
            raise

    def stop(self) -> None:
        """Stop the local HTTP server."""

        if self._server is None:
            return

        self._server.stop()
        self._server = None

        if self._websocket is not None:
            self._websocket.stop()
            self._websocket = None

    def __enter__(self) -> "Runtime":
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
