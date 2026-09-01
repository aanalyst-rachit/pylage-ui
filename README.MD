<div align="center">

# ⚡ PyLage UI

### Build reactive, WebSocket-synced web dashboards — in pure Python. No JS, no build step, no bundler.

[![License: AGPL v3](https://img.shields.io/badge/license-AGPLv3%20%2F%20Commercial-blue.svg)](#-licensing--commercial-model)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Stars](https://img.shields.io/github/stars/aanalyst-rachit/pylage-ui?style=social)](https://github.com/aanalyst-rachit/pylage-ui)

</div>

---

## Why PyLage UI?

Most "Python UI" tools force a trade-off: either you write raw HTML/JS templates, or you get a slow, re-run-the-whole-script reactivity model. PyLage UI takes a different approach — a **real component tree**, **real reactive state**, and a **real diff/patch protocol** over WebSockets, so your Python state and the browser DOM never drift apart.

- 🐍 **Pure Python component model** — `Column`, `Row`, `Button`, `Card`, `Table`... compose UI the way you'd compose functions, no template files.
- 🔌 **Reactive by default** — wrap a value in `State`, call `.set()`, and every bound component patches itself in the browser. No manual DOM wiring.
- 🌲 **Structural diffing, not full re-renders** — the runtime computes minimal `insert` / `remove` / `replace` / `update` operations and ships only what changed.
- 🧱 **Batteries-included layout system** (`pylage_layout`) — `AppShell`, `TwoColumn`, `Sidebar`, `Hero`, `PricingSection`, full page **templates** (`Dashboard`, `AdminPanel`, `Authentication`...) so you're not rebuilding CSS grids from scratch.
- 🎨 **Typed, immutable styling** — `Style` and `ResponsiveStyle` objects with real breakpoints (`sm`/`md`/`lg`/`xl`), plus a `Theme` system that emits CSS custom properties.
- 🧩 **Zero JS authored by you** — the browser runtime (`CLIENT_RUNTIME`) is a small embedded script that speaks the wire protocol; you never touch it.

---

## ✨ Core Features

| Capability | What it means |
|---|---|
| **Reactive `State`** | `pylage.State(value)` — subscribe, mutate via `.set()`, get automatic dependency tracking. |
| **Component Registry** | Every tag (`Button`, `Card`, `Input`...) is backed by a `ComponentRegistry` entry describing its HTML tag, prop kinds (`attribute` / `boolean` / `text`), and reactivity contract. |
| **Batched Updates** | A `Scheduler` + `DirtyNodes` queue coalesces many `.set()` calls in the same tick into **one** WebSocket patch. |
| **Structural Tree Ops** | `component.add()`, `.insert()`, `.replace()`, `.remove()`, `.clear()`, `.set_children()`, `.move_to()` — each broadcasts a matching `tree_add` / `tree_replace` / `tree_remove` / `tree_move` / `tree_clear` / `tree_set_children` message. |
| **35+ Built-in Components** | `Column`, `Row`, `Grid`, `Card`, `Table`, `Form`, `Dialog`, `Tabs`, `Select`, `Slider`, `Switch`, `DatePicker`, `Alert`, `Toast`, `Breadcrumbs`, `Pagination`, `Drawer`, `Tooltip`, `Popover`, `Avatar`, `Badge`, `Accordion`, `Carousel`, `Image`, `Video`, `Audio`, `Icon`, `Canvas`, and more. |
| **Layout & Pattern Library** | `pylage_layout` ships `AppShell`, `Container`, `Stack`, `Split`, `TwoColumn`/`ThreeColumn`, `SidebarLayout`, `Hero`, `PricingSection`, `FAQ`, `Testimonial`, plus full page templates. |
| **Theming** | `Theme(colors=, spacing=, radius=, fonts=)` renders CSS custom properties once per document; `Style` values can reference `var(--color-primary)` directly. |
| **Two-way Input Binding** | Passing a `State` as `Input(value=...)` auto-wires an `on_input` handler that writes keystrokes straight back into your Python state. |
| **Serve or Export** | `pylage.run(app, serve=True)` for a live WebSocket dev server, or `serve=False` (default) to export a static `index.html`. |

---

## 🚀 Quick Start

### 1. Install

```bash
pip install pylage-ui
```

### 2. A reactive counter in 10 lines

This is the canonical "hello reactivity" example — a `State` bound directly into a `Heading`, mutated by a `Button` click handler, live-patched in the browser with zero manual DOM code:

```python
import pylage as pl

count = pl.State(0)

def increment():
    count.set(count.value + 1)   # triggers an automatic WebSocket patch

app = pl.Column(
    pl.Heading(count),                       # bound to State — re-renders on change
    pl.Button("Increment", on_click=increment),
)

pl.run(app, title="Reactive Counter", serve=True, open_browser=True)
```

Run it:

```bash
python app.py
```

A local server + WebSocket runtime spins up, your browser opens automatically, and every click re-renders **only** the `Heading` — not the page.

### 3. A static export (no server)

```python
import pylage as pl

app = pl.Column(
    pl.Heading("Hello, PyLage!"),
    pl.Text("This ships as a single static HTML file."),
)

pl.run(app, title="My App", output="dist/index.html")  # serve=False by default
```

### 4. A dashboard shell with `pylage_layout`

```python
import pylage as pl
from pylage_layout.layouts import AppShell, TwoColumn, Container
from pylage_layout.patterns import Hero, StatsSection

sidebar = pl.Column(pl.Text("Dashboard"), pl.Text("Settings"))

content = Container(
    Hero(
        title="Welcome back",
        description="Here's what changed since your last visit.",
        actions=["View Report"],
    ),
    StatsSection(
        title="Overview",
        stats=[
            {"value": "12.8K", "label": "Users", "description": "+18.4%"},
            {"value": "$48.2K", "label": "Revenue", "description": "+24.1%"},
        ],
    ),
)

app = AppShell(
    header=pl.Text("PyLage Dashboard"),
    content=TwoColumn(sidebar, content),
)

pl.run(app, title="Dashboard", serve=True)
```

---

## 🏗️ Architecture Overview

PyLage UI's reactivity is not "re-run the script on every event." It's a real dependency-tracked patch pipeline:

```
 Python State.set(new_value)
        │
        ▼
 State notifies subscribers (only if value actually changed — `==` check)
        │
        ▼
 StateBinding looks up (Component, prop_name) pairs via DependencyGraph
        │
        ▼
 DirtyNodes.mark(component)        ← component queued, not re-rendered yet
        │
        ▼
 Scheduler.request() → coalesces N marks in the same tick into ONE flush
        │
        ▼
 Scheduler.flush() → resolves final State values → builds an UpdateMessage
        │            (includes registry `prop_meta`: kind + html_name)
        ▼
 WebSocketServer._broadcast(json) → every connected browser tab
        │
        ▼
 CLIENT_RUNTIME (embedded JS) finds the DOM node via `data-pylage-id`
        │
        ▼
 Patches ONLY the changed attribute / textContent / DOM property
```

Structural changes (adding, removing, replacing, or reordering components) follow a parallel path: `Component.add()` / `.replace()` / `.move_to()` etc. fire a `subscribe_mutation` event, which `TreeMutationObserver` turns into `tree_add` / `tree_replace` / `tree_move` / `tree_remove` / `tree_clear` / `tree_set_children` protocol messages — so the browser DOM is patched at the exact grafting point, never by re-rendering an ancestor.

> **Key insight:** the diff granularity is *per-prop*, not per-component. Updating `Button.text` never touches `Button.disabled`, and never touches sibling components at all.

---

## 📖 Developer Manual

### Core Concepts

#### Components

Every visual element is a `Component` — a small dataclass with `type`, `props`, `children`, `events`, and a stable `id`. You never construct `Component(...)` directly; you use the factory functions:

```python
import pylage as pl

card = pl.Card(
    pl.Heading("Plan: Pro"),
    pl.Text("$29/month"),
    class_name="pricing-card",   # → rendered as class="pricing-card"
    title="Pro plan",            # → rendered as title="Pro plan"
)
```

Props fall into three **kinds**, defined per-component in the `ComponentRegistry`:

| Kind | Behavior |
|---|---|
| `attribute` | Rendered as a plain HTML attribute (`value="..."`, `disabled`). |
| `boolean` | Rendered as a bare attribute only when truthy (`disabled`, `checked`). |
| `text` | Becomes the element's **text content**, never an HTML attribute (e.g. `Button(text=...)`, `Heading(text=...)`). |

#### Props

Any keyword argument that isn't a registered prop is passed through as a generic HTML attribute (backward-compatible fallback) — but registry-known props are authoritative for casing (`class_name` → `class`, not `class-name`).

#### Styles — the `Style` object

`pylage.Style` is a **frozen dataclass** with a fixed, explicit field set (`color`, `padding`, `flex_direction`, `border_radius`, `box_shadow`, `gap`, ...). This is intentional: it prevents typo'd CSS properties from silently doing nothing.

```python
from pylage import Style

box = Style(
    display="flex",
    flex_direction="column",
    gap="1rem",
    padding="1.5rem",
    border_radius="0.75rem",
    box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)",
)
```

> ⚠️ **You cannot pass arbitrary CSS keys as fields.** `Style(margin_inline="auto")` will raise a `TypeError` — that field doesn't exist. For anything outside the fixed field set, use `custom`:
>
> ```python
> Style(
>     color="var(--brand)",
>     custom={"--brand": "#7c3aed"},   # keys MUST start with "--"
> )
> ```
> Custom keys that don't start with `--` raise `ValueError` at render time.

For breakpoints, wrap `Style` objects in `ResponsiveStyle`:

```python
from pylage import ResponsiveStyle, Style

responsive = ResponsiveStyle(
    base=Style(flex_direction="column", width="100%"),
    md=Style(flex_direction="row"),     # ≥768px
    lg=Style(gap="2rem"),               # ≥1024px
)
```

`Style` is immutable — `style.color = "red"` raises. To combine a default with an override, use `.merge()`:

```python
merged = default_style.merge(user_style)  # user_style values win where non-None
```

#### Children

Components accept children positionally. `None` values are automatically filtered out, which makes conditional children trivial:

```python
pl.Column(
    pl.Heading("Title"),
    pl.Text("Optional subtitle") if show_subtitle else None,
)
```

---

### Event System

Any keyword prop prefixed with `on_` is extracted as an **event handler**, not a prop — it never leaks into the rendered HTML:

```python
def handle_click():
    print("clicked!")

pl.Button("Save", on_click=handle_click)
```

Handlers can optionally accept a `payload` (used for `on_input` / `on_change`):

```python
def handle_input(payload: dict):
    print(payload["value"])  # the live keystroke value

pl.Input(on_input=handle_input)
```

You can also attach handlers imperatively:

```python
button = pl.Button("Save")
button.on("click", handle_click)
```

#### Best practice: mutating state

There is **no manual `mark_dirty()` call** in PyLage UI — and you should never look for one. Reactivity is fully automatic *as long as you go through `State.set()`*:

```python
count = pl.State(0)

def increment():
    count.set(count.value + 1)   # ✅ triggers dependency graph + scheduler automatically
```

Batch multiple `.set()` calls freely — the `Scheduler` coalesces them into a single patch per tick:

```python
def bulk_update():
    a.set(1)
    b.set(2)
    c.set(3)
    # → exactly ONE flush, ONE WebSocket message, per bound component
```

---

### Layout System

`pylage_layout.layouts` provides composable, responsive primitives — all built on the same `Style` / `ResponsiveStyle` contract:

| Primitive | Purpose |
|---|---|
| `Container(*children)` | Centered, width-constrained (`max-width: 1200px`) responsive wrapper. |
| `Stack(*children)` | Responsive vertical→horizontal flex stack (column on mobile, row ≥`md`). |
| `Split(*children)` | Same responsive contract as `Stack`, semantically for two "sides". |
| `TwoColumn` / `ThreeColumn` | Multi-column responsive `Row` with sensible default gaps. |
| `SidebarLayout(sidebar, content)` | Fixed-width sidebar + fluid content `Row`. |
| `AppShell(header=, sidebar=, content=)` | Canonical app skeleton — header on top, sidebar + content body below. |
| `Center(*children)` | Flex-centers children both axes. |
| `Section(*children)` | Full-width vertical page section with default top/bottom padding. |

```python
from pylage_layout.layouts import AppShell, TwoColumn, Container, Footer

app = AppShell(
    header=pl.Text("My App"),
    content=TwoColumn(
        sidebar,
        Container(main_content),
    ),
)
```

`pylage_layout.patterns` (Hero, FeatureSection, PricingSection, CTA, StatsSection, ContentSection, Testimonial, FAQ, ContactSection, NewsletterSection, SearchBar, BreadcrumbTrail, LoginForm/SignupForm, EmptyState/ErrorState/Loading) and `pylage_layout.templates` (LandingPage, Dashboard, AdminPanel, Authentication, ProfilePage, SettingsPage, Documentation) build on top of these primitives for full-page scaffolding.

---

### State Handling — Gotchas

| ❌ Pitfall | ✅ Fix |
|---|---|
| Mutating a `State`'s inner container in place: `count.value.append(x)` | Reassign via `.set()`: `count.set(count.value + [x])`. `State.set()` only fires subscribers when the **new value differs** (`==` check) from the old one — in-place mutation of a list/dict leaves the reference identical and silently no-ops. |
| Passing a plain Python value where the framework expects to track it reactively, e.g. `Heading(some_variable)` where `some_variable` is a `str`, then mutating `some_variable` later | Wrap it in `State` up front: `Heading(pl.State(some_variable))`. Only `State`-backed props are diffed and re-pushed to the browser. |
| Assigning arbitrary CSS keys to `Style(...)` (e.g. `Style(backdropFilter=...)`) | `Style` is a closed dataclass — unsupported fields raise `TypeError` at construction. Use the `custom={"--token": value}` escape hatch (keys **must** start with `--`) and reference it with `var(--token)`. |
| Trying to mutate a `Style` instance after creation (`style.color = "red"`) | `Style` and `Theme` are frozen/immutable. Build a new one, or `.merge()` an override on top of a default. |
| Registering a non-reactive prop and expecting UI updates on `.set()` | Some registry props are declared `reactive=False` (opt-out contract). Check the component's `PropDefinition` — reactivity is per-prop, not just per-component. |
| Expecting a `State` change to re-render *children* of a component | State bindings are per-**prop**, not structural. To swap out entire subtrees reactively, use `component.set_children(...)` / `.replace(...)` inside your event handler — these emit their own `tree_*` patch messages. |
| Calling `.set()` with the exact same value expecting a forced re-render | It's a no-op by design (`old_value == value` short-circuits). If you need to force a redraw, change the value (even trivially, e.g. toggle a version counter). |

---

## ⚖️ Licensing & Commercial Model

PyLage UI is **dual-licensed**:

- **🆓 Community Edition** — [GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.en.html). Free to use, modify, and self-host, provided that any network-accessible service built on PyLage UI also makes its complete corresponding source available under AGPL v3.
- **🏢 Commercial License** — required for proprietary SaaS products, closed-source distribution, or enterprise deployments that cannot comply with AGPL's network copyleft clause. Includes priority support and indemnification options.

> Unsure which applies to you? Open a [licensing inquiry](https://github.com/aanalyst-rachit/pylage-ui/issues/new?labels=licensing) before shipping to production.

---

## 🤝 Community & Contribution

- **Bugs:** open an [issue](https://github.com/aanalyst-rachit/pylage-ui/issues) with a minimal reproduction (a `Component` tree + the `State` mutation that triggers the problem is usually enough).
- **Feature requests / RFCs:** start a [discussion](https://github.com/aanalyst-rachit/pylage-ui/discussions) before opening a PR for anything touching the wire protocol, registry contract, or `Style` schema.
- **Pull requests:**
  1. Fork → branch (`feat/...` / `fix/...`).
  2. Add or update tests under `test/` — the suite covers the registry contract, diff/patch engine, scheduler batching, and WebSocket broadcast behavior; regressions here block merges.
  3. Run `pytest` locally before opening the PR.
- **Roadmap priorities:** expanding the component registry's prop contracts, first-class conditional/list rendering helpers, and a CLI scaffolding tool for `pylage_layout` templates.

---

<div align="center">

**Built for developers who want reactive UIs without leaving Python.**

[Documentation](#) · [Examples](#) · [Discussions](https://github.com/aanalyst-rachit/pylage-ui/discussions) · [Issues](https://github.com/aanalyst-rachit/pylage-ui/issues)

</div>