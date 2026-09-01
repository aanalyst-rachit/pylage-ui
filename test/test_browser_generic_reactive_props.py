import re

from pathlib import Path

from pylage.runtime.client import CLIENT_RUNTIME


print("=== PYLAGE BROWSER GENERIC REACTIVE PROP TEST ===")


# ------------------------------------------------------------
# 1. Runtime must contain generic reactive update handling.
# ------------------------------------------------------------

assert "Object.keys(message.props)" in CLIENT_RUNTIME

print("Generic prop iteration: PASS")


# ------------------------------------------------------------
# 2. Client must NOT contain one-off prop-name dispatch.
# ------------------------------------------------------------

for prop_name in (
    "text",
    "value",
    "disabled",
    "class",
    "title",
):
    pattern = rf'propName\s*===\s*["\']{re.escape(prop_name)}["\']'

    assert not re.search(pattern, CLIENT_RUNTIME), (
        f"Hard-coded reactive prop dispatch remains: {prop_name!r}"
    )

print("No hard-coded reactive prop dispatch: PASS")


# ------------------------------------------------------------
# 3. Runtime should use generic DOM attribute/property logic.
# ------------------------------------------------------------

generic_markers = (
    "setAttribute",
    "removeAttribute",
)

assert any(
    marker in CLIENT_RUNTIME
    for marker in generic_markers
), "Generic DOM attribute patching not found."

print("Generic DOM patching: PASS")


# ------------------------------------------------------------
# 4. Keep the client runtime source available for inspection.
# ------------------------------------------------------------

client_source = Path("pylage/runtime/client.py").read_text(
    encoding="utf-8"
)

assert 'CLIENT_RUNTIME = r"""' in client_source

print("Embedded client runtime: PASS")


print()
print("=== BROWSER GENERIC REACTIVE PROP TEST PASS ===")
