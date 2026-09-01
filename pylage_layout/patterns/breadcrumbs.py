"""Breadcrumb pattern for PyLage Layout."""

from typing import Any

from pylage.components import Breadcrumbs


def BreadcrumbTrail(
    *children: Any,
    class_name: str | None = None,
    **props: Any,
):
    if class_name is not None:
        props["class_name"] = class_name

    return Breadcrumbs(*children, **props)


__all__ = ["BreadcrumbTrail"]
