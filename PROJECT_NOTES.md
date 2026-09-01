Aapke poore bug log aur issues ko thoroughly analyze karke sabhi duplicates ko merge kar diya gaya hai aur ek clean, module-wise consolidated **Master Bug Tracking List** tayyar ki gayi hai.


### **1. CORE ENGINE & RUNTIME SYSTEM (`pylage/core/` & `pylage/runtime/`)**

* **1.1 Constructor Keywords & Props Normalization (`TypeError` / `AttributeError`)**
* **Issue:** Base `Component` class directly `.attrs` ya `.style` attributes expose nahi karti aur `Component(tag="...", style=...)` jaisa keyword signature reject kar deti hai.
* **Fix:** `Component.__init__` ko update karein taaki `tag` ke alawa `style` (`Style` instance) aur `props` dict ko optional kwargs accept karke `self.props` me properly normalize kar sake.


* **1.2 WebSocket Event Protocol & Event Binding Data Loss**
* **Issue:** Client-to-backend WebSocket messages parse karte waqt event parser dynamic context attributes (`checked` for toggles/radios, `selectedIndex` for dropdowns, etc.) ko drop kar deta hai aur generic `change` events properly bind nahi hote.
* **Fix:** `parse_client_event` me frontend payload se `target.value`, `target.checked`, aur `target.selected` fields extract karein. `pylage/core/binding.py` me non-interactive wrappers par click bubbling/delay aur `click-outside` listeners handle karein.


* **1.3 Re-rendering Pipeline & Native DOM Method Invocations**
* **Issue:** Text node re-rendering partial fail hoti hai, conditional rendering (`True/False`) me sub-tree off-screen overlay containers update nahi hote, aur native JavaScript methods (e.g., `<dialog>` ke `.showModal()` / `.close()`) invoke karne ke bajaye runtime sirf HTML properties pass karta hai.
* **Fix:** Core DOM engine me diffing & sub-tree re-render fix karein aur lifecycle me native JS method execution support add karein.


* **1.4 Style & CSS Unit Auto-Conversion**
* **Issue:** Numeric state values (jaise `ProgressBar` width ya `Spinner` animation duration) bina `%` ya `px` suffix ke pass hone par CSS bind breakdown hota hai ya bounds Clip nahi hote (value > 100 ya negative overflow).
* **Fix:** `pylage/styling/style.py` me numeric sanitization enforce karein.



---

### **2. FORM CONTROLS & INPUTS (`pylage/components/forms.py`, `basic.py`, `switch.py`)**

* **2.1 `Input()` Keyword Argument Collision (`TypeError`)**
* **Issue:** `Input()` wrapper function default `value=""` aur `**props` me clashing parameters handle nahi kar pata. Custom type (e.g., `type="checkbox"` ya `type="info"`) pass karne par `TypeError: component() got multiple values for argument 'type'` exception aati hai.
* **Fix:** Signature me `input_type="text"` accept karein aur `props` dictionary se `type` key ko safely pop karke cleanup ke saath internal component me pass karein.


* **2.2 Select Dropdown Options Invisibility & Value Sync**
* **Issue:** `<select>` serialize karte waqt `<option>` child nodes strip/ignore ho jaate hain, jisse dropdown blank/collapsed dikhta hai. Iske alawa `event.target.value` change par backend state update disconnect rehta hai.
* **Fix:** `Select` aur `Option` components ki dedicated classes banayein aur `on("change")` handler par raw payload extract karke Python `State` ko notify karein.


* **2.3 Radio Group Input & Layout Rendering Bug**
* **Issue:** Options ke label text aur radio inputs standard DOM wrappers (`<label>`, `<span>`) me wrap nahi hote. Inputs/buttons pure render tree se gayab ho jaate hain aur options transparent background ki wajah se dikhte nahi hain.
* **Fix:** `RadioGroup` container ko flex-row `<label>` element structure me render karein, jisme explicit `<input type="radio">` aur `<span>` text container styled colors (`#0f172a`) ke saath apply ho.


* **2.4 Switch / Checkbox State Inversion & Styling Failure**
* **Issue:** Checkbox attributes HTML string me strip ho rahe hain, visual dimensions bina empty div render hote hain, aur modern switch control ke bajaye normal `[x]` checkbox dikhte hain. Boolean `checked` state update karne par parser sync break hota hai.
* **Fix:** Dedicated `Switch` / `Checkbox` wrappers banayein, `checked` attribute ko direct `State.value` se link karein, aur `change`/`click` event handler me boolean state invert (`State.set(not State.value)`) support karein.


* **2.5 Form Submission Data Capture Failure**
* **Issue:** Native `<form>` submission page reload trigger kar deti hai aur child inputs ki aggregate values auto-extract nahi hoti.
* **Fix:** `Form` wrapper class create karein jo native submit ko intercept (`e.preventDefault()`) karke child input states ka structured payload Python dictionary me emit kare.


* **2.6 Slider Track & DatePicker Input Failures**
* **Issue:** `type="range"` input aur `type="date"` controls me track/thumb va browser-native pickers strip ho rahe hain aur state change values propagate nahi hoti.
* **Fix:** Custom `Slider` aur `DatePicker` classes banayein jo custom/native CSS-styled DOM attributes pass karke events correctly capture karein.



---

### **3. DATA & FEEDBACK COMPONENTS (`pylage/components/`)**

* **3.1 Table Component (Sorting & Pagination Bugs)**
* **Issue:** Multi-page data par search/filter apply karne se page index reset nahi hota (out-of-index error), aur mixed numbers/strings columns sort karne par ASCII or dict type errors aate hain.
* **Fix:** Filter trigger par page index auto-reset karein aur sort comparator me robust type-casting add karein.


* **3.2 Alert & Toast Components (DOM Leaks & Overlay Blocking)**
* **Issue:** Alert dismiss karne par CSS se `display: none` hota hai par Python DOM tree me object retained rehta hai (re-render par dubara reappear hota hai). Multiple Toasts ek saath fire hone par z-index overlap, timer stack overflow, aur UI freeze ka risk hota hai.
* **Fix:** Client JS side par auto-hide timers, z-index stack management, aur Python tree removal sync add karein.


* **3.3 Spinner & ProgressBar (Async Blocking & Value Overflow)**
* **Issue:** Async Python functions ke dauran GIL / event loop block hone se spinner animation task khatam hone se pehle freeze rehta hai. ProgressBar bound clipping missing hai.
* **Fix:** Event loop non-blocking async dispatch implement karein aur ProgressBar values ko 0-100 range me clamp karein.


* **3.4 Skeleton, Badge, Accordion & Carousel Issues**
* **Issue:**
* **Skeleton:** Dimensions explicitly pass na ho to container collapse hota hai (Layout Shift - CLS).
* **Badge:** Long text par `text-overflow: ellipsis` truncation missing hone se parent flexbox distort hota hai.
* **Accordion:** Single-expand mode me doosra section kholne par pehle wale ka internal state active reh jata hai.
* **Carousel:** In-active tab me autoplay timer chalne se memory leak hoti hai, aur mobile touch/swipe events capture nahi hote.


* **Fix:** CSS truncation/dimensions apply karein, active section state sync strictly manage karein, aur tab visibility API integrated timers + touch event listeners introduce karein.



---

### **4. LAYOUT & ADVANCED NAVIGATION (`pylage/components/layout.py` & others)**

* **4.1 Layout Container CSS & Spacing Failure**
* **Issue:** `Card`, `Row`, `Column`, aur `Container` classes ke CSS inline styles ya utility classes missing hain, jiske kaaran UI plain HTML flow me stack dikhta hai (bina padding/shadows/alignment).
* **Fix:** Layout primitives ke flex/grid alignment styles aur default utility classes enforce karein.


* **4.2 Missing Primitives & Overlay Components (Pagination, Drawer, Popover, Dialog)**
* **Issue:** `Pagination`, `Drawer`, `Popover`, aur `Dialog/Modal` target components component registry me missing hain, dynamic positionable DOM bindings break hain, ya off-screen/overlay visibility correct toggle nahi ho rahi.
* **Fix:** Native JS overlay hooks aur official wrapper classes build karein.


* **4.3 Entrypoint & Demo Integration (`main.py`)**
* **Issue:** Manual demo test scripts (`data_feedback_manual.py` etc.) main app entrypoint se missing hain aur proper runtime serving setup config structured nahi hai.
* **Fix:** `main.py` entrypoint update karke saare manuals ko interactive test suites ke roop me link karein.