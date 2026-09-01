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
