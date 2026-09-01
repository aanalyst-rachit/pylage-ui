from pylage.core.registry import ComponentRegistry, PropDefinition


print("=== PYLAGE PROP REACTIVE CONTRACT TEST ===")

registry = ComponentRegistry()


# ------------------------------------------------------------
# 1. Valid boolean values must work.
# ------------------------------------------------------------

for reactive in (True, False):
    registry.register(
        f"Reactive_{reactive}",
        "div",
        props={
            "value": PropDefinition(
                "value",
                reactive=reactive,
            )
        },
    )

print("Boolean reactive values: PASS")


# ------------------------------------------------------------
# 2. Non-boolean values must be rejected.
# ------------------------------------------------------------

invalid_values = (
    "true",
    "false",
    1,
    0,
    None,
    [],
)

for invalid in invalid_values:
    try:
        registry.register(
            f"Invalid_{type(invalid).__name__}",
            "div",
            props={
                "value": PropDefinition(
                    "value",
                    reactive=invalid,
                )
            },
        )
    except (ValueError, TypeError):
        continue

    raise AssertionError(
        f"Invalid reactive value was accepted: {invalid!r}"
    )

print("Non-boolean reactive rejection: PASS")


print()
print("=== PROP REACTIVE CONTRACT PASS ===")
