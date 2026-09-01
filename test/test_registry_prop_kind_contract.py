from pylage.core.registry import ComponentRegistry, PropDefinition


print("=== PYLAGE PROP KIND CONTRACT TEST ===")


registry = ComponentRegistry()


# ------------------------------------------------------------
# 1. Supported kinds must work.
# ------------------------------------------------------------

for kind in (
    "attribute",
    "boolean",
    "text",
):
    registry.register(
        f"Component_{kind}",
        "div",
        props={
            "value": PropDefinition(
                "value",
                kind=kind,
            )
        },
    )

print("Supported prop kinds: PASS")


# ------------------------------------------------------------
# 2. Invalid kinds must be rejected.
# ------------------------------------------------------------

try:
    registry.register(
        "InvalidComponent",
        "div",
        props={
            "value": PropDefinition(
                "value",
                kind="banana",
            )
        },
    )
except (ValueError, TypeError):
    print("Invalid prop kind rejection: PASS")
else:
    raise AssertionError(
        "Invalid prop kind was accepted: 'banana'"
    )


# ------------------------------------------------------------
# 3. Empty kind must also be rejected.
# ------------------------------------------------------------

try:
    registry.register(
        "EmptyKindComponent",
        "div",
        props={
            "value": PropDefinition(
                "value",
                kind="",
            )
        },
    )
except (ValueError, TypeError):
    print("Empty prop kind rejection: PASS")
else:
    raise AssertionError(
        "Empty prop kind was accepted"
    )


print()
print("=== PROP KIND CONTRACT PASS ===")
