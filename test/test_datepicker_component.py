from pylage import DatePicker
from pylage.core.renderer import render


def test_datepicker_renders_as_date_input():
    datepicker = DatePicker()

    html = render(datepicker)

    assert "<input" in html
    assert 'type="date"' in html


def test_datepicker_supports_props():
    datepicker = DatePicker(
        class_name="date-field",
        title="Select date",
        value="2026-08-30",
    )

    html = render(datepicker)

    assert 'class="date-field"' in html
    assert 'title="Select date"' in html
    assert 'value="2026-08-30"' in html


def test_datepicker_supports_min_max():
    datepicker = DatePicker(
        min="2026-01-01",
        max="2026-12-31",
    )

    html = render(datepicker)

    assert 'min="2026-01-01"' in html
    assert 'max="2026-12-31"' in html


def test_datepicker_state_renders_initial_value():
    from pylage import State

    selected = State("2026-08-30")
    datepicker = DatePicker(value=selected)

    html = render(datepicker)

    assert 'value="2026-08-30"' in html


def test_datepicker_state_updates_from_input_event():
    from pylage import State
    from pylage.core.events import EventDispatcher

    selected = State("2026-08-30")
    datepicker = DatePicker(value=selected)

    dispatcher = EventDispatcher(datepicker)

    dispatcher.dispatch(
        datepicker.id,
        "input",
        {"value": "2026-09-01"},
    )

    assert selected.value == "2026-09-01"


def test_datepicker_state_updates_from_change_event():
    from pylage import State
    from pylage.core.events import EventDispatcher

    selected = State("2026-08-30")
    datepicker = DatePicker(
        value=selected,
        on_change=lambda payload: selected.set(payload["value"]),
    )

    dispatcher = EventDispatcher(datepicker)

    dispatcher.dispatch(
        datepicker.id,
        "change",
        {"value": "2026-09-01"},
    )

    assert selected.value == "2026-09-01"
