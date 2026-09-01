from pylage.core.registry import ComponentRegistry, PropDefinition


print("=== PYLAGE PROP HTML NAME CONTRACT TEST ===")

registry = ComponentRegistry()


# ------------------------------------------------------------
# 1. None is valid — renderer falls back to prop name.
# ------------------------------------------------------------

registry.register(
    "DefaultNameComponent",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            html_name=None,
        )
    },
)

print("None html_name: PASS")


# ------------------------------------------------------------
# 2. Valid HTML name must work.
# ------------------------------------------------------------

registry.register(
    "CustomNameComponent",
    "div",
    props={
        "class_name": PropDefinition(
            "class_name",
            html_name="class",
        )
    },
)

print("Valid html_name: PASS")


# ------------------------------------------------------------
# 3. Empty HTML name must be rejected.
# ------------------------------------------------------------

try:
    registry.register(
        "EmptyHTMLNameComponent",
        "div",
        props={
            "value": PropDefinition(
                "value",
                html_name="",
            )
        },
    )
except (ValueError, TypeError):
    print("Empty html_name rejection: PASS")
else:
    raise AssertionError(
        "Empty html_name was accepted"
    )


# ------------------------------------------------------------
# 4. Non-string HTML name must be rejected.
# ------------------------------------------------------------

try:
    registry.register(
        "InvalidHTMLNameComponent",
        "div",
        props={
            "value": PropDefinition(
                "value",
                html_name=123,
            )
        },
    )
except (ValueError, TypeError):
    print("Non-string html_name rejection: PASS")
else:
    raise AssertionError(
        "Non-string html_name was accepted"
    )


print()
print("=== PROP HTML NAME CONTRACT PASS ===")
