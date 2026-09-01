from pylage.core.component import Component
from pylage.core.tree import collect_ids, count_components


def test_collect_ids_returns_empty_for_non_component():
    assert collect_ids("hello") == []
    assert collect_ids(None) == []


def test_count_components_returns_zero_for_non_component():
    assert count_components("hello") == 0
    assert count_components(None) == 0


def test_collect_ids_walks_nested_component_tree():
    root = Component(type="Column")
    heading = Component(type="Heading")
    button = Component(type="Button")
    nested = Component(type="Column")
    text = Component(type="Text")

    root.add(heading, nested)
    nested.add(button, text)

    assert collect_ids(root) == [
        root.id,
        heading.id,
        nested.id,
        button.id,
        text.id,
    ]


def test_count_components_counts_nested_components_only():
    root = Component(type="Column")
    heading = Component(type="Heading")
    nested = Component(type="Column")
    button = Component(type="Button")

    root.add(heading, "plain text", nested)
    nested.add(button, 123)

    assert count_components(root) == 4


def test_collect_ids_preserves_duplicate_ids():
    root = Component(type="Column", id="same")
    first = Component(type="Button", id="same")
    second = Component(type="Text", id="same")

    root.add(first, second)

    assert collect_ids(root) == [
        "same",
        "same",
        "same",
    ]


def test_count_components_does_not_depend_on_component_ids():
    root = Component(type="Column", id="same")
    first = Component(type="Button", id="same")
    second = Component(type="Text", id="same")

    root.add(first, second)

    assert count_components(root) == 3


def test_print_tree_prints_nested_components_and_text(capsys):
    from pylage.core.tree import print_tree

    root = Component(type="Column")
    child = Component(
        type="Button",
        props={"text": "Hello"},
    )

    root.add(child, "plain text")

    print_tree(root)

    output = capsys.readouterr().out

    assert f"Column [{root.id}]" in output
    assert f"Button [{child.id}]" in output
    assert "props={'text': 'Hello'}" in output
    assert "plain text" in output


def test_print_tree_handles_non_component(capsys):
    from pylage.core.tree import print_tree

    print_tree("hello")

    output = capsys.readouterr().out

    assert output == "'hello'\n"
