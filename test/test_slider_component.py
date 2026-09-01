from pylage import Slider
from pylage.core.renderer import render


def test_slider_renders_as_range():
    slider = Slider()

    html = render(slider)

    assert "<input" in html
    assert 'type="range"' in html


def test_slider_supports_props():
    slider = Slider(
        class_name="volume-slider",
        title="Volume",
    )

    html = render(slider)

    assert 'class="volume-slider"' in html
    assert 'title="Volume"' in html


def test_slider_supports_value():
    slider = Slider(value=50)

    html = render(slider)

    assert 'value="50"' in html


def test_slider_supports_min_max_step():
    slider = Slider(
        min=0,
        max=100,
        step=5,
    )

    html = render(slider)

    assert 'min="0"' in html
    assert 'max="100"' in html
    assert 'step="5"' in html


def test_slider_state_renders_initial_value():
    from pylage import State

    selected = State(25)
    slider = Slider(value=selected)

    html = render(slider)

    assert 'value="25"' in html


def test_slider_state_updates_from_input_event():
    from pylage import State
    from pylage.core.events import EventDispatcher

    selected = State(25)
    slider = Slider(value=selected)

    dispatcher = EventDispatcher(slider)

    dispatcher.dispatch(
        slider.id,
        "input",
        {"value": "75"},
    )

    assert selected.value == "75"


def test_slider_state_updates_reactive_callback():
    from pylage import State
    from pylage.core.binding import StateBinding

    selected = State(25)
    slider = Slider(value=selected)
    updates = []

    StateBinding(
        slider,
        lambda component, props: updates.append(
            (component, props)
        ),
    )

    selected.set(75)

    assert updates == [
        (slider, {"value": 75}),
    ]
