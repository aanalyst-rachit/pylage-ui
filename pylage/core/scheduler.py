from __future__ import annotations

from typing import Callable
import threading

from pylage.core.component import Component
from pylage.core.dirty import DirtyNodes


class Scheduler:
    """Batches dirty component updates."""

    def __init__(
        self,
        dirty: DirtyNodes,
        callback: Callable[[Component], None],
        schedule_flush: Callable[[], None] | None = None,
    ) -> None:
        self.dirty = dirty
        self.callback = callback
        self.schedule_flush = schedule_flush
        self._flush_requested = False
        self._lock = threading.Lock()

    def request(self) -> None:
        """Request one coalesced flush from the owning runtime."""

        if self.schedule_flush is None:
            return

        with self._lock:
            if self._flush_requested:
                return

            self._flush_requested = True

        self.schedule_flush()

    def flush(self) -> None:
        with self._lock:
            self._flush_requested = False

        nodes = self.dirty.nodes()
        self.dirty.clear()

        for node in nodes:
            self.callback(node)
