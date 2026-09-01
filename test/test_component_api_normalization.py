import pytest

from pylage.core.component import Component


def test_component_preserves_canonical_props_api():
    component = Component(
        type="div",
        props={"role": "region"},
        children=["Hello"],
    )

    assert component.type == "div"
    assert component.props == {"role": "region"}
    assert component.children == ["Hello"]


def test_component_accepts_direct_html_props():
    component = Component(
        type="input",
        placeholder="Enter name",
        disabled=True,
    )

    assert component.type == "input"
    assert component.props == {
        "placeholder": "Enter name",
        "disabled": True,
    }


def test_component_accepts_tag_alias():
    component = Component(
        tag="button",
        title="Save",
    )

    assert component.type == "button"
    assert component.props["title"] == "Save"


def test_component_normalizes_style():
    style = {"color": "red"}

    component = Component(
        type="div",
        style=style,
    )

    assert component.props["style"] is style


def test_component_merges_props_attrs_and_direct_props():
    component = Component(
        type="input",
        props={"placeholder": "Props"},
        attrs={"autocomplete": "name"},
        required=True,
        style={"width": "100%"},
    )

    assert component.props == {
        "placeholder": "Props",
        "autocomplete": "name",
        "required": True,
        "style": {"width": "100%"},
    }


def test_component_direct_props_override_props_and_attrs():
    component = Component(
        type="input",
        props={"placeholder": "Props"},
        attrs={"placeholder": "Attrs"},
        placeholder="Direct",
    )

    assert component.props["placeholder"] == "Direct"


def test_component_rejects_conflicting_type_and_tag():
    with pytest.raises(TypeError, match="conflicting"):
        Component(type="div", tag="span")


def test_component_requires_type_or_tag():
    with pytest.raises(TypeError, match="requires"):
        Component()


def test_component_preserves_explicit_internal_identity():
    component = Component(
        type="div",
        id="component-identity",
    )

    assert component.id == "component-identity"


def test_component_rejects_invalid_props_container():
    with pytest.raises(TypeError, match="props"):
        Component(
            type="div",
            props=["invalid"],  # type: ignore[arg-type]
        )
