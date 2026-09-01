import pylage as ps
from pylage.core.renderer import render


def _radio(value, *, name="choice", **props):
    return ps.Input(
        input_type="radio",
        name=name,
        value=value,
        **props,
    )


def test_radio_group_renders_radio_options():
    group = ps.RadioGroup(
        _radio("a"),
        _radio("b"),
    )

    html = render(group)

    assert "<div" in html
    assert 'type="radio"' in html
    assert 'value="a"' in html
    assert 'value="b"' in html


def test_radio_group_preserves_option_order():
    group = ps.RadioGroup(
        _radio("a"),
        _radio("b"),
        _radio("c"),
    )

    html = render(group)

    assert html.index('value="a"') < html.index('value="b"')
    assert html.index('value="b"') < html.index('value="c"')


def test_radio_group_supports_props():
    group = ps.RadioGroup(
        _radio("a"),
        class_name="choice-group",
        title="Choose one",
    )

    html = render(group)

    assert 'class="choice-group"' in html
    assert 'title="Choose one"' in html


def test_radio_group_value_selects_matching_radio():
    group = ps.RadioGroup(
        _radio("male"),
        _radio("female"),
        value="female",
    )

    html = render(group)

    assert 'value="female" checked' in html
    assert 'value="male" checked' not in html


def test_radio_group_value_supports_state():
    selected = ps.State("male")

    group = ps.RadioGroup(
        _radio("male"),
        _radio("female"),
        value=selected,
    )

    html = render(group)

    assert 'value="male" checked' in html
    assert 'value="female" checked' not in html

    selected.set("female")

    html = render(group)

    assert 'value="female" checked' in html
    assert 'value="male" checked' not in html


def test_radio_group_change_event_is_registered():
    received = []

    group = ps.RadioGroup(
        _radio("male"),
        _radio("female"),
        on_change=lambda payload: received.append(payload),
    )

    html = render(group)

    assert 'data-pylage-events="change"' in html


def test_radio_group_registry_declares_value_as_reactive():
    from pylage.core.registry import registry

    definition = registry.get("RadioGroup")

    assert definition is not None
    assert definition.props is not None
    assert "value" in definition.props
    assert definition.props["value"].reactive is True


def test_radio_group_existing_component_contract_is_preserved():
    group = ps.RadioGroup()

    assert group.type == "RadioGroup"
    assert group.children == []
