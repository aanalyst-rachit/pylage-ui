
# PyLage Development Tracker (Master Consolidated)

> **Purpose:** PyLage ke identified bugs, form controls, runtime protocol, dynamic tree lifecycle, thread-safety, aur architecture gaps ko structured tarike se track karna.
> 
> 

---

## Project Workflow

Har task ka lifecycle:

```text
TODO
  ↓
ANALYZING
  ↓
VERIFIED
  ↓
IN PROGRESS
  ↓
TESTING
  ↓
COMPLETE

```

### Status Rules

* `[ ]` — Not started
* `[~]` — In progress
* `[?]` — Requires verification
* `[x]` — Completed
* `[!]` — Blocked

---

# PHASE A — CORE FOUNDATION & RECTIFICATION

**Goal:** Component API, event protocol, state binding contract aur structural resilience ko stable banana.

---

## A1 — Component API & Props Normalization

**Status:** `[x] COMPLETE` | **Priority:** `CRITICAL`

### Completion Summary

* Direct HTML props `Component.props` mein normalize.
* `style=` aur `tag=` alias supported.
* Invalid containers aur conflicting `type`/`tag` values validated.
* A1 regression suite: **10 passed**, Full suite: **582 passed**.

---

## A2 — Unified Browser Event Payload Protocol

**Status:** `[x] COMPLETE` | **Priority:** `CRITICAL`

### Completion Summary

* Standard event payload schema browser → backend sync verified for all input controls (`value`, `checked`, `selectedIndex`, multi-select).



---

## A3 — Controlled State Binding Contract

**Status:** `[x] COMPLETE` | **Priority:** `CRITICAL`

### Completion Summary

* Bidirectional controlled input sequence (`Input(value=State)`) synchronized without infinite loops.



---

## A4 — Input Type API Collision

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

### Completion Summary

* Component `type` aur HTML input `type` separated using `input_type` strategy.



---

## A5 — Component Identity & Matrix Equality Guard (Bug C3)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

### Problem

`Component` default `@dataclass` equality (`__eq__`) use karta hai. NumPy arrays/pandas objects matching scan par `ValueError` throw karte hain aur `.remove()` / `.replace()` O(subtree size) comparison force karte hain.

### Work

* [ ] `@dataclass(eq=False)` set karke strict reference identity (`is`) enforce karna.


* [ ] Child mutations (`remove`, `replace`) ko O(1) identity matching par shift karna.


* [ ] Matrix/DataFrame prop component removal test add karna.



---

## A6 — `State.set()` Cycle Detection & Safe Equality (Bug C4)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

### Problem

Synchronous binding mein circular state update raw `RecursionError` throw karta hai. NumPy arrays par `old_value == value` direct check crash karta hai.

### Work

* [ ] `State` mein re-entrancy flag (`_notifying`) aur `CircularStateDependencyError` exception add karna.


* [ ] `State.set()` equality check mein `try-except` guard add karke identity fallback implement karna.


* [ ] Circular dependency detection test add karna.



---

# PHASE B — FORM CONTROLS

**Goal:** All major form controls ko reliable browser rendering aur Python State integration dena.

---

## B1 — Select & Option

**Status:** `[x] COMPLETE` | **Priority:** `CRITICAL`

---

## B2 — Checkbox

**Status:** `[x] COMPLETE` | **Priority:** `CRITICAL`

---

## B3 — Switch

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

---

## B4 — RadioGroup

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

---

## B5 — Form Submission

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

---

## B6 — Slider

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

---

## B7 — DatePicker

**Status:** `[x] COMPLETE` | **Priority:** `HIGH`

---

# PHASE C — RUNTIME & DOM ENGINE

**Goal:** Dynamic DOM operations, reactive index updates, aur browser imperative messaging ko fully reliable banana.

---

## C1 — Dynamic Tree Snapshot Desync (`StateBinding` & `EventDispatcher`) (Bug C1)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

### Goal

Server startup ke baad dynamic nodes (`.add()`, `.insert()`, `.replace()`) ki reactivity aur click event dispatchers ko live sync karna.

### Work

* [ ] `EventDispatcher` mein `index(node)` aur `deindex(node)` public hooks add karna.


* [ ] `StateBinding` mein `bind_tree(node)` aur `unbind_tree(node)` hooks add karna.


* [ ] `WebSocketServer._on_tree_mutation` se bind/unbind aur index/deindex hooks wire karna.


* [ ] Dynamic subtree insertion & removal tests add karna.



---

## C2 — Multi-Tenant Isolation & Thread-Safe Registry (Bug C2)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

### Goal

Global `ComponentRegistry` singleton ke cross-tenant leaks aur race conditions ko eliminate karna.

### Work

* [ ] `ComponentRegistry` mein `RLock` lock ke saath atomic `register_if_missing()` method implement karna.


* [ ] `WebSocketServer` mein per-app `registry_instance` injection point provide karna.


* [ ] Multi-tenant isolation aur race condition tests add karna.



---

## C3 — Dynamic Client Event Delegation Binding (Bug C6)



**Status:** `[ ] TODO` | **Priority:** `HIGH`

### Goal

Client runtime Hardcoded (`click`, `input`, `change`) listeners ke bajaye dynamic `on_<event>` support kare.

### Work

* [ ] JS runtime mein `ensureEventTypeBound(eventType)` dynamic listener implementation.


* [ ] Page load aur dynamic DOM mutations (`tree_add`, `tree_replace`) par `data-pylage-events` read karke capture/bubble mode mein bind karna.


* [ ] `on_submit`, `on_focus`, `on_keydown` browser dispatch tests add karna.



---

## C4 — Server Event Response & Error Protocol (Bug C7)



**Status:** `[ ] TODO` | **Priority:** `HIGH`

### Goal

Backend response message errors (`{"type":"response","ok":false}`) client level par visual logging aur callbacks surface karein.

### Work

* [ ] `window.PyLage.onResponse` mein `message.type === "response"` branch support add karna.


* [ ] `window.PyLage.onError` fallback hook provide karna.



---

## C5 — DOM Command Protocol (Original C1)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

---

## C6 — Dialog Lifecycle (Original C2)



**Status:** `[ ] TODO` | **Priority:** `CRITICAL`

---

## C7 — Drawer / Popover / Overlay System (Original C3)



**Status:** `[ ] TODO` | **Priority:** `HIGH`

---

## C8 — Conditional & Dynamic Subtree Rendering (Original C4)



**Status:** `[ ] TODO` | **Priority:** `HIGH`

---

# PHASE D — RESILIENCE & ARCHITECTURAL RISKS

**Goal:** Background updates, threads, serialization, aur transport safety faults handle karna.

---

## D1 — Batch Exception Isolation in `Scheduler.flush()` (Bug C5)



**Status:** `[ ] TODO` | **Priority:** `HIGH`

### Work

* [ ] `Scheduler.flush()` ke node iteration par try-except isolation wrap karna taaki ek component failure remaining batch ko silent drop na kare.



---

## D2 — Thread-Safe `DirtyNodes` Pipeline (Bug H3)



**Status:** `[ ] TODO` | **Priority:** `MEDIUM`

### Work

* [ ] `DirtyNodes` class ke inner storage operations ko `threading.Lock()` se guard karna.



---

## D3 — Dual Parent Notification on `move_to()` (Bug H1)



**Status:** `[ ] TODO` | **Priority:** `MEDIUM`

### Work

* [ ] `Component.move_to()` call par `old_parent` aur `new_parent` dono ke subscribers ko tree mutation payload broadcast karna.



---

## D4 — WebSocket Auto-Reconnect & Client Offline Banner (Bug H2)



**Status:** `[ ] TODO` | **Priority:** `MEDIUM`

### Work

* [ ] Client JS websocket socket close hone par exponential backoff retry network loop implement karna.


* [ ] `window.PyLage.onConnectionChange` lifecycle hook surface karna.



---

## D5 — HTML Attribute Props Serialization & Strict Booleans (Bugs H4 & H5)



**Status:** `[ ] TODO` | **Priority:** `MEDIUM`

### Work

* [ ] Component-as-prop aur non-`on_` functions pass karne par `TypeError` throw karna.


* [ ] Unregistered boolean props values `False` hone par raw `"False"` string generate hone se block karke attribute omit karna.



---

## D6 — FIFO WebSocket Delivery Worker Queue (Bug H6)



**Status:** `[ ] TODO` | **Priority:** `LOW`

### Work

* [ ] N independent tasks ki jagah ek strict FIFO `asyncio.Queue` worker pipe establish karna.



---

# PHASE E — DATA & FEEDBACK COMPONENTS

* **E1 — ProgressBar Validation** `[ ] TODO`

* **E2 — Spinner & Async Behavior** `[ ] TODO`

* **E3 — Alert Lifecycle** `[ ] TODO`

* **E4 — Toast System** `[ ] TODO`

* **E5 — Skeleton** `[ ] TODO`

* **E6 — Badge** `[ ] TODO`

* **E7 — Accordion** `[ ] TODO`

* **E8 — Carousel** `[ ] TODO`


---

# PHASE F — LAYOUT & STYLE ARCHITECTURE

* **F1 — Core Layout Primitives (Card, Row, Column)** `[ ] TODO`

* **F2 — PyLage Layout Integration** `[ ] TODO`

* **F3 — Extended CSS Primitives on `Style` (Bug S1)** `[ ] TODO`

* Add `z_index`, `transform`, `transition`, `pointer_events`, `outline`, `visibility`, per-side borders.





---

# PHASE G — TABLE AUDIT & INFRASTRUCTURE CLEANUP

* **G1 — Table Sorting Verification** `[?] REQUIRES VERIFICATION`

* **G2 — Table Filtering Verification** `[?] REQUIRES VERIFICATION`

* **G3 — Table Pagination Verification** `[?] REQUIRES VERIFICATION`

* **G4 — Legacy Backup File Cleanup (Bug P1)** `[ ] TODO`

* Delete obsolete backup files (`*.before_*`, `*.v01`, `*.bak`).




* **G5 — Demo Hub Showcase** `[ ] TODO`


---