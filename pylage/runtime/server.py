from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Optional
from urllib.parse import urlparse


class _RequestHandler(BaseHTTPRequestHandler):
    directory: Path
    filename: str = "index.html"

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path not in ("/", f"/{self.filename}"):
            self.send_error(404, "Not Found")
            return

        try:
            content = self.directory.joinpath(
                self.filename
            ).read_bytes()
        except FileNotFoundError:
            self.send_error(
                404,
                f"{self.filename} not found",
            )
            return

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(content)),
        )
        self.end_headers()
        self.wfile.write(content)

    def log_message(
        self,
        format: str,
        *args: object,
    ) -> None:
        return


class LocalServer:
    """Small local HTTP server for a rendered PyLage app."""

    def __init__(
        self,
        directory: str | Path,
        host: str = "127.0.0.1",
        port: int = 0,
        filename: str = "index.html",
    ) -> None:
        self.directory = Path(directory).resolve()
        self.host = host
        self.port = port
        self.filename = Path(filename).name

        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[Thread] = None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("Server is not running.")

        return (
            f"http://{self.host}:"
            f"{self._server.server_port}/"
        )

    def start(self) -> str:
        if self._server is not None:
            raise RuntimeError("Server is already running.")

        handler = type(
            "PyLageRequestHandler",
            (_RequestHandler,),
            {
                "directory": self.directory,
                "filename": self.filename,
            },
        )

        self._server = ThreadingHTTPServer(
            (self.host, self.port),
            handler,
        )

        self._thread = Thread(
            target=self._server.serve_forever,
            daemon=True,
        )
        self._thread.start()

        return self.url

    def stop(self) -> None:
        if self._server is None:
            return

        self._server.shutdown()
        self._server.server_close()

        if self._thread is not None:
            self._thread.join(timeout=2)

        self._thread = None
        self._server = None

    def __enter__(self) -> "LocalServer":
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
