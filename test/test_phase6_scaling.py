from time import perf_counter

from pylage.core.component import Component
from pylage.core.snapshot import component_to_snapshot
from pylage.core.diff import diff
from pylage.core.patch import operations_to_messages


def _build_tree(count: int) -> Component:
    root = Component(type="Column")

    for index in range(count - 1):
        root.add(
            Component(
                type="Text",
                props={"text": f"Node {index}"},
            )
        )

    return root


def _measure(fn):
    start = perf_counter()
    result = fn()
    elapsed = perf_counter() - start
    return result, elapsed


def test_phase6_component_scaling():
    print()
    print("===== PHASE 6 — COMPONENT SCALING =====")
    print()

    for count in (10, 100, 1000, 10000):
        root = _build_tree(count)

        snapshot, snapshot_time = _measure(
            lambda: component_to_snapshot(root)
        )

        current = snapshot.copy()
        current["children"] = list(snapshot["children"])

        if current["children"]:
            current["children"][0] = {
                **current["children"][0],
                "props": {
                    **current["children"][0]["props"],
                    "text": "Updated",
                },
            }

        operations, diff_time = _measure(
            lambda: diff(snapshot, current)
        )

        messages, patch_time = _measure(
            lambda: operations_to_messages(operations)
        )

        assert snapshot["id"] == root.id
        assert len(snapshot["children"]) == count - 1
        assert len(operations) == 1
        assert len(messages) == 1

        print(f"nodes              : {count}")
        print(f"snapshot           : {snapshot_time:.9f}s")
        print(f"diff               : {diff_time:.9f}s")
        print(f"patch              : {patch_time:.9f}s")
        print()
