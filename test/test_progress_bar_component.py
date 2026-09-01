from pylage import ProgressBar
from pylage.core.renderer import render


def test_progress_bar_renders_as_progress():
    progress = ProgressBar()

    html = render(progress)

    assert "<progress" in html


def test_progress_bar_supports_props():
    progress = ProgressBar(
        class_name="upload-progress",
        title="Uploading",
        value=50,
        max=100,
    )

    html = render(progress)

    assert 'class="upload-progress"' in html
    assert 'title="Uploading"' in html
    assert 'value="50"' in html
    assert 'max="100"' in html


def test_progress_bar_supports_text():
    progress = ProgressBar(
        text="Uploading...",
    )

    html = render(progress)

    assert "Uploading..." in html
