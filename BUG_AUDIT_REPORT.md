# PyLage UI — Deep Bug Audit & Architectural Code Review

Scope: `pylage/core/*`, `pylage/runtime/*`, `pylage/components/basic.py`, `pylage/styling/*`, `pylage/renderers/html.py`.
Methodology: static trace of every function referenced below against the real implementation, cross-checked against the existing test suite to confirm which behaviors are *intended* vs. *accidental*.

---

## 🔴 CRITICAL BUGS

### C1. Static Tree Snapshot Desync — `StateBinding` and `EventDispatcher` never re-index mutated subtrees

**Location:** `pylage/core/binding.py::StateBinding.__init__` / `pylage/core/events.py::EventDispatcher.__init__`, both consumed once in `pylage/runtime/websocket.py::WebSocketServer.__init__`.

**Root Cause:**
Both subsystems build their internal index (`StateBinding._bind_tree(root)`, `EventDispatcher._index_tree(root)`) **exactly once**, at server construction time. `TreeMutationObserver` (the thing that *does* react to `add()` / `insert()` / `replace()` / `set_children()`) is a completely separate object with zero coupling to either subsystem — it only exists to turn structural mutations into `tree_add` / `tree_replace` / ... WebSocket messages for DOM patching. Nothing in the codebase re-runs `_bind_tree` or `_index_tree` when the component tree changes after startup.

Consequence:
- Any component **added after the server starts** (`root.add(new_button)`) whose props reference a `State` object will **never receive UpdateMessages**, because `value.subscribe(...)` was never called for it. The browser will render its initial value and then freeze forever, no matter how many times you `.set()` the underlying state.
- Any component added after startup with an `on_click` (or any) handler will raise `KeyError: Unknown component id: <id>` the first time a user clicks it, because `EventDispatcher._components` never learned about it.

**Reproduction Case:**
```python
import pylage as pl
from pylage.runtime.websocket import WebSocketServer

root = pl.Column()
server = WebSocketServer(root)
server.start()

# Simulate "dynamic UI" - e.g. adding a row after the dashboard is live
count = pl.State(0)

def increment():
    count.set(count.value + 1)   # will NEVER reach the browser

new_row = pl.Row(
    pl.Heading(count),                    # dead reactivity
    pl.Button("Increment", on_click=increment),  # clicking raises KeyError server-side
)
root.add(new_row)   # tree_add IS broadcast — the DOM node appears...
                     # ...but it's inert. Click it and the server replies
                     # {"type":"response","ok":false,"error":"Unknown component id: ..."}
```

**The Fix:** give `StateBinding` and `EventDispatcher` public `bind`/`unbind` entry points, keyed per-node so subtrees can be added *and removed* cleanly, then wire `WebSocketServer._on_tree_mutation` to call them for every structural mutation type.

```python
# pylage/core/events.py
class EventDispatcher:
    def index(self, node: Any) -> None:
        """Public hook: register a newly-inserted subtree."""
        self._index_tree(node)

    def deindex(self, node: Any) -> None:
        """Public hook: remove a detached subtree from dispatch."""
        if not isinstance(node, Component):
            return
        self._components.pop(node.id, None)
        for child in node.children:
            self.deindex(child)
```

```python
# pylage/core/binding.py
class StateBinding:
    def __init__(self, root, callback, graph=None, dirty=None, scheduler=None):
        self.root = root
        self.callback = callback
        self.graph = graph
        self.dirty = dirty
        self.scheduler = scheduler
        # was: self._subscriptions: list[Callable[[], None]]
        # now tracked per-node so a subtree can be precisely unbound later
        self._node_bindings: dict[str, list[tuple[State, str, Callable[[], None]]]] = {}
        self._bind_tree(root)

    def _bind_tree(self, node: Any) -> None:
        if not isinstance(node, Component):
            return
        for prop_name, value in node.props.items():
            if not isinstance(value, State) or not self._is_reactive(node, prop_name):
                continue
            unsubscribe = value.subscribe(
                lambda old, new, component=node, name=prop_name:
                    self._changed(component, name, new)
            )
            self._node_bindings.setdefault(node.id, []).append(
                (value, prop_name, unsubscribe)
            )
            if self.graph is not None:
                self.graph.add_dependency(value, node, prop_name)
        for child in node.children:
            self._bind_tree(child)

    def bind_tree(self, node: Any) -> None:
        """Public hook: bind a subtree added after initial construction."""
        self._bind_tree(node)

    def unbind_tree(self, node: Any) -> None:
        """Public hook: fully detach a removed subtree (fixes C? leak too)."""
        if not isinstance(node, Component):
            return
        for child in list(node.children):
            self.unbind_tree(child)
        for state, prop_name, unsubscribe in self._node_bindings.pop(node.id, []):
            unsubscribe()
            if self.graph is not None:
                self.graph.remove_dependency(state, node, prop_name)

    def stop(self) -> None:
        for bindings in self._node_bindings.values():
            for state, prop_name, unsubscribe in bindings:
                unsubscribe()
        self._node_bindings.clear()
```

```python
# pylage/runtime/websocket.py — inside _on_tree_mutation
if mutation_type == "add":
    for child in event.get("children", []):
        if isinstance(child, Component):
            self._binding.bind_tree(child)
            self._dispatcher.index(child)
    # ... existing broadcast logic

if mutation_type in ("remove", "clear"):
    for child in event.get("children", []):
        if isinstance(child, Component):
            self._binding.unbind_tree(child)
            self._dispatcher.deindex(child)
    # ... existing broadcast logic

if mutation_type == "replace":
    old_child, new_child = event.get("old_child"), event.get("new_child")
    if isinstance(old_child, Component):
        self._binding.unbind_tree(old_child)
        self._dispatcher.deindex(old_child)
    if isinstance(new_child, Component):
        self._binding.bind_tree(new_child)
        self._dispatcher.index(new_child)
    # ... existing broadcast logic
```
Apply the same unbind-old/bind-new pairing to `set_children`.

---

### C2. Global mutable `ComponentRegistry` singleton — zero multi-tenant isolation, TOCTOU race

**Location:** `pylage/core/registry.py` (`registry = ComponentRegistry()` at module scope), consumed implicitly by `pylage/components/basic.py`.

**Root Cause:** There is exactly **one** `ComponentRegistry` instance per Python process, imported by reference everywhere (`from pylage.core.registry import registry`). Several built-in factories use a lazy "register on first use" pattern:

```python
def Card(*children, **props):
    from pylage.core.registry import PropDefinition, registry
    if not registry.has("Card"):
        registry.register("Card", "div", props={...})
    return component("Card", *children, **props)
```

Two failure modes:
1. **No isolation between apps.** If you host multiple independent `pylage-ui` dashboards in one process (e.g. a FastAPI app spinning up a `WebSocketServer` per tenant/session — the exact deployment model this framework targets), and *any* tenant calls `registry.register("Card", "section", renderer=custom)` to theme their own Card, **every other tenant's Card silently starts using that renderer too.** There is no `registry_instance` plumbed through `pl.run()` / `Runtime` / `WebSocketServer` by default — they all fall back to the shared global.
2. **`has()` + `register()` is not atomic.** Two threads (e.g. two concurrent WebSocket connections both rendering a `Card` for the first time) can both observe `registry.has("Card") is False` before either has registered it, then both call `register()` — a classic read-check-write race with "last write wins" semantics on shared state.

**Reproduction Case:**
```python
from pylage.core.registry import registry, PropDefinition
import pylage as pl

# Tenant A customizes Card globally...
registry.register("Card", "section", props={
    "class_name": PropDefinition("class_name", kind="attribute", html_name="class"),
})

# Tenant B, in a totally separate WebSocketServer instance, never opted in —
# but gets Tenant A's tag change anyway:
from pylage.core.renderer import render
print(render(pl.Card("hi")))   # <section ...>hi</section>  — NOT <div>
```

**The Fix:** make the registry injectable end-to-end, and make lazy registration atomic.

```python
# pylage/core/registry.py
import threading

class ComponentRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, ComponentDefinition] = {}
        self._lock = threading.RLock()

    def register_if_missing(self, type: str, tag: str, **kwargs) -> ComponentDefinition:
        """Atomic has()+register() — closes the TOCTOU window."""
        with self._lock:
            existing = self._definitions.get(type)
            if existing is not None:
                return existing
            return self.register(type, tag, **kwargs)
```

```python
# pylage/components/basic.py
def Card(*children, **props):
    from pylage.core.registry import PropDefinition, registry
    registry.register_if_missing("Card", "div", props={...})   # atomic
    return component("Card", *children, **props)
```

```python
# pylage/runtime/websocket.py — allow per-app isolation
class WebSocketServer:
    def __init__(self, root, *, host="127.0.0.1", port=0, registry_instance=None):
        self._registry = registry_instance or registry   # opt-in isolation
        ...
    def _get_component_definition(self, component):
        return self._registry.get(component.type)
```
Document clearly: **for any multi-tenant deployment, construct a dedicated `ComponentRegistry()` per app/session and pass it explicitly** — never rely on the process-wide default outside single-app usage.

---

### C3. `Component`'s auto-generated deep `__eq__` breaks identity-based tree mutation and can crash on common prop types

**Location:** `pylage/core/component.py::Component` (the `@dataclass` decorator, undecorated with `eq=False`).

**Root Cause:** `Component` is a plain `@dataclass`. Dataclasses generate `__eq__` by default, comparing **every field** — `type`, `props`, `children`, `events`, `id`, even `_parent` and `_mutation_subscribers`. But `Component.remove()`, `.replace()`, and `.move_to()` all rely on `list.remove(x)` / `list.index(x)`, which use `==`, not `is`:

```python
def remove(self, child):
    self.children.remove(child)     # ← uses __eq__, deep-compares props/children recursively
```

Two concrete problems:

1. **Correctness/perf:** removing/replacing a child in a list of siblings forces Python to deep-compare `props` dicts (and recursively, nested `children`) for every sibling scanned before the match — expensive for large trees, and semantically wrong for a mutable, reference-identity node type that already has an explicit `id`-based `__hash__`.
2. **Crash risk:** if two components (even unrelated ones) share a prop key whose value doesn't support unambiguous `==` — the most common real case being a NumPy array or pandas object passed as chart/table data — the *dict* equality check underneath `__eq__` raises:
   `ValueError: The truth value of an array with more than one element is ambiguous.`
   This crash can be triggered by `.remove()`/`.replace()` targeting an **entirely unrelated sibling**, because `list.remove` scans left-to-right and evaluates `==` against every element until (if ever) it finds the real match.

**Reproduction Case:**
```python
import numpy as np
import pylage as pl

col = pl.Column(
    pl.Table(data=np.array([1, 2, 3])),   # sibling #1 — unrelated to what we're removing
    target := pl.Text("remove me"),
)

col.remove(target)   # ValueError: truth value of an array is ambiguous
                      # (raised while scanning sibling #1's props for a match, NOT target)
```

**The Fix:** give `Component` identity semantics explicitly — it already has an explicit `id`-based `__hash__`, so equality should match:

```python
# pylage/core/component.py
@dataclass(eq=False)   # ← identity-based __eq__/`is` semantics, matching __hash__
class Component:
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Child] = field(default_factory=list)
    events: dict[str, EventHandler] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    ...
    def __hash__(self) -> int:
        return hash(self.id)
```
With `eq=False`, Python falls back to `object.__eq__` (identity), so `list.remove` / `list.index` / `in` now compare by `is`, matching every other place in the file that already does ancestor-cycle checks via `is`. This eliminates the crash risk entirely and makes every mutation method O(1) comparison per element instead of O(subtree size).

---

### C4. Unbounded synchronous recursion in `State.set()` — no cycle guard, no NumPy-safe equality

**Location:** `pylage/core/state.py::State.set()`; `pylage/core/binding.py::StateBinding._changed()`.

**Root Cause — two compounding bugs in the same function:**

**(a) No re-entrancy/cycle detection.** `StateBinding` supports a documented, tested "immediate callback" mode with **no scheduler** (`StateBinding(root, callback, graph=graph)` — see `test_state_binding_graph.py`, `test_reactive_pipeline.py`). In that mode, `_changed()` calls `self.callback(...)` **synchronously**, from inside `State.set()`'s own subscriber loop. If that callback (directly, or transitively through app logic) calls `.set()` on a state that circularly depends back on the original — nothing stops it. `State.set()` has zero re-entrancy protection.

**(b) `old_value == value` can raise or misbehave for common types.** No comparison is guarded. NumPy arrays raise `ValueError` on truthy-coercion of `==`; mutable containers (`list`/`dict`) mutated in place and then re-`.set()` with the *same reference* are always seen as unchanged (since `old_value is value`, so trivially `==`), silently swallowing legitimate updates.

**Reproduction Case (stack overflow via circular dependency, no scheduler):**
```python
import pylage as pl
from pylage.core.binding import StateBinding

a = pl.State(0)
b = pl.State(0)

a.subscribe(lambda old, new: b.set(new + 1))   # A changes → bump B
b.subscribe(lambda old, new: a.set(new + 1))   # B changes → bump A

a.set(1)
# RecursionError: maximum recursion depth exceeded
# — no error message pointing at the cycle, just a raw Python traceback
```

**The Fix:**
```python
# pylage/core/state.py
from __future__ import annotations
from typing import Any, Callable

Subscriber = Callable[[Any, Any], None]


class CircularStateDependencyError(RuntimeError):
    """Raised when a State.set() call re-enters the same State mid-notification."""


class State:
    def __init__(self, value: Any = None):
        self._value = value
        self._subscribers: list[Subscriber] = []
        self._notifying = False   # re-entrancy guard

    @property
    def value(self) -> Any:
        return self._value

    def set(self, value: Any) -> None:
        old_value = self._value

        try:
            unchanged = bool(old_value == value)
        except (ValueError, TypeError):
            # NumPy / pandas / custom __eq__ that can't coerce to bool —
            # fall back to identity rather than crashing the whole update.
            unchanged = old_value is value

        if unchanged:
            return

        if self._notifying:
            raise CircularStateDependencyError(
                "State.set() was called re-entrantly on the same State "
                "instance while it was still notifying subscribers. "
                "This indicates a circular dependency between States — "
                "break the cycle instead of chaining .set() calls in subscribers."
            )

        self._value = value
        self._notifying = True
        try:
            for subscriber in tuple(self._subscribers):
                subscriber(old_value, value)
        finally:
            self._notifying = False
```
This turns a silent, unhelpful `RecursionError` into an immediate, actionable exception naming the actual problem, and eliminates the NumPy crash class entirely.

---

### C5. `Scheduler.flush()` has no exception isolation — one bad component silently drops the entire batch

**Location:** `pylage/core/scheduler.py::Scheduler.flush()`.

**Root Cause:**
```python
def flush(self):
    with self._lock:
        self._flush_requested = False
    nodes = self.dirty.nodes()
    self.dirty.clear()          # ← cleared BEFORE processing
    for node in nodes:
        self.callback(node)     # ← no try/except
```
`dirty.clear()` runs before the loop. If `self.callback(node)` raises for *any* node in the batch (e.g. a prop value that fails JSON serialization inside `WebSocketServer._scheduled_update` → `_json_safe`), the exception propagates out of `flush()` immediately — **every remaining node in that batch is silently dropped**, because they were already removed from `DirtyNodes` and there's no retry/requeue. This is a genuine, silent state-desync: N-1 components in a batch never reach the browser because component N happened to throw.

**Reproduction Case:**
```python
class Unserializable:
    def __repr__(self): raise RuntimeError("boom")

good = pl.Heading(pl.State("fine"))
bad  = pl.Heading(pl.State(Unserializable()))   # ok until read
app  = pl.Column(good, bad)

# ... inside a WebSocketServer session:
good.props["text"].set("updated 1")   # marked dirty
bad.props["text"].set("updated 2")    # marked dirty — will raise during _json_safe/str()
# flush() throws → `good`'s "updated 1" update is NEVER sent, even though
# it had nothing to do with the failure.
```

**The Fix:**
```python
# pylage/core/scheduler.py
import logging

logger = logging.getLogger("pylage.scheduler")

class Scheduler:
    def flush(self) -> None:
        with self._lock:
            self._flush_requested = False

        nodes = self.dirty.nodes()
        self.dirty.clear()

        for node in nodes:
            try:
                self.callback(node)
            except Exception:
                # Isolate the failure to this node only — never let one bad
                # component silently kill updates for the rest of the batch.
                logger.exception(
                    "pylage: failed to flush update for component %r; "
                    "skipping this node, remaining batch continues.",
                    getattr(node, "id", node),
                )
```

---

### C6. Client-side runtime only wires up 3 hardcoded DOM event types — every other `on_<event>` handler is dead code

**Location:** `pylage/runtime/client.py::CLIENT_RUNTIME` (bottom):
```js
document.addEventListener("click", handleEvent);
document.addEventListener("input", handleEvent);
document.addEventListener("change", handleEvent);
```

**Root Cause:** The Python API happily accepts *any* `on_<name>=handler` keyword (`component.py::component()` strips every `on_`-prefixed kwarg into `events[name]` with no allow-list). The renderer faithfully emits `data-pylage-events="submit,focus,keydown"` etc. into the DOM. But the browser runtime only ever registers **document-level delegated listeners for `click`, `input`, and `change`** — nothing else. Any handler for `on_submit`, `on_focus`, `on_blur`, `on_keydown`, `on_mouseover`, `on_dblclick`, etc. is silently unreachable: the API surface promises support it doesn't deliver, with no error at registration time, render time, or runtime.

**Reproduction Case:**
```python
form = pl.Form(on_submit=lambda: print("never called"))
# renders: <form data-pylage-events="submit" ...>
# — but no `document.addEventListener("submit", ...)` exists client-side.
# Submitting the form does nothing. No error anywhere.
```

**The Fix:** bind event types dynamically as they're discovered in the DOM, instead of hardcoding three:

```js
// pylage/runtime/client.py — inside CLIENT_RUNTIME
const boundEventTypes = new Set();

function ensureEventTypeBound(eventType) {
    if (boundEventTypes.has(eventType)) return;
    boundEventTypes.add(eventType);
    // focus/blur don't bubble — need capture phase
    const useCapture = eventType === "focus" || eventType === "blur";
    document.addEventListener(eventType, handleEvent, useCapture);
}

function bindEventsFromAttribute(eventsAttr) {
    if (!eventsAttr) return;
    eventsAttr.split(",").forEach(function (name) {
        ensureEventTypeBound(name.trim());
    });
}

// 1. Bind everything already present on initial page load:
document.querySelectorAll("[data-pylage-events]").forEach(function (el) {
    bindEventsFromAttribute(el.getAttribute("data-pylage-events"));
});

// 2. Bind anything that arrives later via tree_add / tree_replace / tree_set_children —
//    call bindEventsFromAttribute(item.events) inside createTreeNode() wherever
//    `element.setAttribute("data-pylage-events", item.events)` currently happens.
```
And replace the three hardcoded calls at the bottom of the file with the initial-scan call above. This makes *every* `on_<event>` the Python API allows actually work, for both initial and dynamically-inserted nodes.

---

### C7. Server-side event errors are parsed but never surfaced to the user — silent click failures

**Location:** `pylage/runtime/client.py::CLIENT_RUNTIME`, `window.PyLage.onResponse`.

**Root Cause:** `WebSocketServer._handle()` correctly catches dispatch exceptions and replies with `EventMessageResponse.error(str(exc))` → `{"type":"response","ok":false,"error":"..."}`. But `onResponse` on the client has no branch for `message.type === "response"` at all:

```js
window.PyLage.onResponse = window.PyLage.onResponse || function (message) {
    console.log("[PyLage response]", message);
    if (!message) { return; }
    if (message.type === "tree_move") { ...; return; }
    // ... 5 more tree_* branches ...
    if (message.type !== "update") { return; }   // ← "response" falls through here and exits
    ...
```
Every event-dispatch failure (including the C1 "unknown component id" case, or *any* Python exception raised inside a click handler) is logged once via `console.log` and then discarded. There is no error toast, no visual feedback, no distinction between success and failure — from the user's perspective the button just did nothing.

**The Fix:**
```js
window.PyLage.onResponse = window.PyLage.onResponse || function (message) {
    console.log("[PyLage response]", message);
    if (!message) { return; }

    if (message.type === "response") {
        if (!message.ok) {
            console.error("[PyLage] Event handler failed:", message.error);
            if (typeof window.PyLage.onError === "function") {
                window.PyLage.onError(message.error);   // apps can hook a toast/alert here
            }
        }
        return;
    }

    // ... existing tree_* / update handling unchanged ...
};
```

---

## 🟡 HIGH / MEDIUM RISKS

| # | Location & Cause | The Fix |
|---|---|---|
| **H1** | `WebSocketServer._on_tree_mutation`: `move_to()` only fires on `new_parent._mutation_subscribers`, never `old_parent`'s — inconsistent with `add`/`remove`/`replace`/`clear`, which all notify the acting parent. Harmless *today* only because `WebSocketServer` uses one global root-level observer subscribed to every node; breaks for any node-scoped `subscribe_mutation()` listener (a documented public API). | In `Component.move_to()`, notify **both** `old_parent._mutation_subscribers` and `new_parent._mutation_subscribers` with the same event payload. |
| **H2** | No WebSocket reconnect logic in `CLIENT_RUNTIME`. On disconnect (`socket.addEventListener("close", ...)`), the socket is dropped and never retried. Every click after that silently falls into the "not ready" branch of `sendEvent()` and is dropped (routed to `onEvent`, which just `console.log`s by default). A dev-server restart or transient network blip permanently kills an open tab with zero recovery and zero user feedback. | Add exponential-backoff reconnect in the `close` handler: `setTimeout(() => connectWebSocket(url), backoff)`, capped and reset on successful reconnect; surface connection state via an optional `window.PyLage.onConnectionChange` hook so apps can show a "reconnecting..." banner. |
| **H3** | `pylage/core/dirty.py::DirtyNodes` (`_nodes`/`_ordered_nodes`) and `pylage/core/registry.py::_definitions` are plain, unlocked collections. `State.set()` can legitimately be called from any thread (e.g. a background job updating dashboard state), which reaches `DirtyNodes.mark()` concurrently with `Scheduler.flush()` reading/clearing the same structures on the event-loop thread — a genuine TOCTOU race that can silently drop a mark (`nodes()` snapshot taken, then `clear()`, with a `mark()` from another thread interleaved in between and lost). | Add a `threading.Lock` around `mark()` / `nodes()` / `clear()` in `DirtyNodes`, matching the discipline already used in `Scheduler`. |
| **H4** | `HTMLRenderer._render_prop_attributes`: any prop value that isn't `None`/`True`/registered-boolean/registered-text falls through to `str(value)`. A `Component` instance passed as a **prop** (not a child) gets `Component.__repr__`'d directly into an HTML attribute — dumping internal Python structure into the page and silently orphaning any handlers/children nested inside it (they never reach `_render_children`). A bare `lambda` passed as a non-`on_`-prefixed prop renders as `"<function <lambda> at 0x7f...>"` — a non-deterministic memory address leaking into markup. | Add an explicit type guard before the generic fallback: `if isinstance(value, Component): raise TypeError(f"Prop {name!r} received a Component instance — pass it as a child, not a prop.")`; similarly reject bare callables that aren't `on_`-prefixed with a clear `TypeError` instead of silently stringifying them. |
| **H5** | Same function: an unregistered/default-kind prop set to Python `False` renders as the literal string `foo="False"` (falls to the generic `else` branch), while `True` correctly renders as a bare attribute. This is inconsistent HTML-boolean handling and leaks a Python-ism (`"False"` is not a meaningful HTML attribute value) for any custom component that doesn't explicitly register `kind="boolean"`. | Normalize: for **any** prop kind, if `value is False` and not explicitly `kind="text"`, omit the attribute entirely (mirroring the registered-boolean behavior), rather than only special-casing `True`. |
| **H6** | `WebSocketServer._on_state_change` calls `asyncio.run_coroutine_threadsafe(self._broadcast(...), self._loop)` **once per dirty node**, as fire-and-forget, from inside `Scheduler.flush()` — which itself already runs on the loop thread (so `run_coroutine_threadsafe` is being (mis)used for same-thread scheduling). Because each call spawns an independent Task, there's no strict ordering guarantee between multiple broadcasts queued in quick succession if any one `connection.send()` experiences backpressure — a later state update could theoretically reach a slow client before an earlier one. | Replace N independent fire-and-forget broadcasts with a single `asyncio.Queue` + one consumer task per server that drains messages strictly in FIFO order, guaranteeing wire ordering regardless of individual `send()` latency. |

---

## 🟢 LOW / DX IMPROVEMENTS

- **Missing common CSS fields on `Style`.** No `z_index`, `transform`, `transition`, `text_transform`, `text_decoration`, `letter_spacing`, `white_space`, `outline`, `visibility`, `pointer_events`, or per-side `border_top`/`border_right`/`border_bottom`/`border_left`. `z_index` in particular is close to a functional gap, not just DX polish — `Dialog`, `Popover`, `Tooltip`, and `Drawer` all need explicit stacking control and currently require the `custom={"--z": ...}` escape hatch plus `z-index:var(--z)` boilerplate for something that should be a first-class field.
- **`Style.merge()` has no "explicitly unset" sentinel.** Since `None` means "inherit from base," there's no way for an override `Style` to explicitly clear a field back to nothing — only to leave it inherited or set to a concrete value.
- **Stale backup files committed inside the real package tree**: `pylage/core/registry.py.before_builtin_prop_contracts`, `registry.py.before_prop_html_name`, `registry.py.before_set_renderer`, `registry.py.before_prop_metadata`, `registry.py.before_registry_builtin_callbacks`, `registry.py.before_renderer_callbacks`, `registry.py.before_props_api`, `registry.py.before_prop_definition`, `component.py.v01`, `client.py.v01`, `renderer.py.phase8-theme-backup`, `protocol.py.bak`. These sit as siblings of the real modules (not excluded via packaging config), ship dead/superseded code with already-fixed bugs, and invite accidental copy-paste regressions. Delete them — that's what `git log` is for.
- **`EventMessageResponse` protocol is entirely dead on the client** outside of the C7 fix — worth adding a lightweight integration test asserting a failed dispatch actually surfaces somewhere observable, not just that the server *sent* the right JSON.
- **API-vs-implementation drift** in general: several public capabilities (`on_<arbitrary event>`, `subscribe_mutation` on non-root nodes, `StateBinding` without a scheduler) are correctly implemented Python-side but silently under-supported at the browser or wiring layer. Worth a "supported event types" and "supported binding modes" section in the docs until C1/C6 land.

---

## Summary Priority Order

1. **C1** (dead reactivity/events on dynamic UI) — blocks the framework's core selling point for any app that mutates its tree after startup.
2. **C2** (registry singleton) — blocks safe multi-tenant/production deployment entirely.
3. **C4** (recursion/circular state) — silent crash with no diagnostic, reachable via documented public API.
4. **C3** (dataclass eq) — crash risk on a very ordinary prop type (NumPy/pandas), plus needless O(n·subtree) mutation cost.
5. **C5, C6, C7** — silent-failure class of bugs; individually less catastrophic but collectively mean "nothing tells you when something breaks," which is the worst failure mode for a framework this young.
