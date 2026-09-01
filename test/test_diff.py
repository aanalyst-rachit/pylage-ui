from pylage.core.diff import diff


def snapshot(
    node_id,
    *,
    type="Text",
    props=None,
    children=None,
    events="",
):
    return {
        "id": node_id,
        "type": type,
        "tag": "div",
        "events": events,
        "props": props or {},
        "children": children or [],
    }


def test_identical_snapshots_produce_no_operations():
    current = snapshot(
        "root",
        props={"text": "Hello"},
    )

    assert diff(current, current) == []


def test_prop_change_produces_one_update():
    previous = snapshot(
        "heading",
        props={"text": "Hello"},
    )
    current = snapshot(
        "heading",
        props={"text": "World"},
    )

    assert diff(previous, current) == [
        {
            "type": "update",
            "id": "heading",
            "props": {"text": "World"},
            "remove_props": [],
        }
    ]


def test_added_prop_is_updated():
    previous = snapshot(
        "button",
        props={"text": "Save"},
    )
    current = snapshot(
        "button",
        props={
            "text": "Save",
            "disabled": True,
        },
    )

    assert diff(previous, current) == [
        {
            "type": "update",
            "id": "button",
            "props": {"disabled": True},
            "remove_props": [],
        }
    ]


def test_removed_prop_is_reported():
    previous = snapshot(
        "button",
        props={
            "text": "Save",
            "disabled": True,
        },
    )
    current = snapshot(
        "button",
        props={"text": "Save"},
    )

    assert diff(previous, current) == [
        {
            "type": "update",
            "id": "button",
            "props": {},
            "remove_props": ["disabled"],
        }
    ]


def test_event_change_produces_event_operation():
    previous = snapshot(
        "button",
        props={"text": "Save"},
        events="click",
    )
    current = snapshot(
        "button",
        props={"text": "Save"},
        events="click,focus",
    )

    assert diff(previous, current) == [
        {
            "type": "events",
            "id": "button",
            "events": "click,focus",
        }
    ]


def test_child_prop_change_is_recursive():
    previous = snapshot(
        "root",
        children=[
            snapshot(
                "child",
                props={"text": "Before"},
            )
        ],
    )

    current = snapshot(
        "root",
        children=[
            snapshot(
                "child",
                props={"text": "After"},
            )
        ],
    )

    assert diff(previous, current) == [
        {
            "type": "update",
            "id": "child",
            "props": {"text": "After"},
            "remove_props": [],
        }
    ]


def test_child_insert_produces_one_insert():
    previous = snapshot("root")

    current = snapshot(
        "root",
        children=[
            snapshot(
                "child",
                type="Button",
                props={"text": "Click"},
            )
        ],
    )

    assert diff(previous, current) == [
        {
            "type": "insert",
            "parent_id": "root",
            "index": 0,
            "node": current["children"][0],
        }
    ]


def test_child_remove_produces_one_remove():
    previous = snapshot(
        "root",
        children=[
            snapshot("child"),
        ],
    )
    current = snapshot("root")

    assert diff(previous, current) == [
        {
            "type": "remove",
            "parent_id": "root",
            "id": "child",
            "index": 0,
        }
    ]


def test_node_type_change_produces_replace():
    previous = snapshot(
        "node",
        type="Text",
        props={"text": "Hello"},
    )
    current = snapshot(
        "node",
        type="Button",
        props={"text": "Hello"},
    )

    assert diff(previous, current) == [
        {
            "type": "replace",
            "id": "node",
            "node": current,
        }
    ]


def test_multiple_changes_are_deterministic():
    previous = snapshot(
        "root",
        props={"class": "old"},
        children=[
            snapshot(
                "first",
                props={"text": "A"},
            ),
            snapshot(
                "removed",
                props={"text": "B"},
            ),
        ],
    )

    current = snapshot(
        "root",
        props={"class": "new"},
        children=[
            snapshot(
                "first",
                props={"text": "Changed"},
            ),
            snapshot(
                "added",
                props={"text": "C"},
            ),
        ],
    )

    assert diff(previous, current) == [
        {
            "type": "update",
            "id": "root",
            "props": {"class": "new"},
            "remove_props": [],
        },
        {
            "type": "remove",
            "parent_id": "root",
            "id": "removed",
            "index": 1,
        },
        {
            "type": "update",
            "id": "first",
            "props": {"text": "Changed"},
            "remove_props": [],
        },
        {
            "type": "insert",
            "parent_id": "root",
            "index": 1,
            "node": current["children"][1],
        },
    ]
