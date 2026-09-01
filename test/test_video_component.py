from pylage import Video
from pylage.core.renderer import render


def test_video_creates_video_component():
    video = Video()

    assert video.type == "Video"


def test_video_renders_as_video():
    video = Video(
        src="movie.mp4",
        controls=True,
    )

    html = render(video)

    assert "<video" in html
    assert 'src="movie.mp4"' in html
    assert "controls" in html
    assert "</video>" in html


def test_video_supports_props():
    video = Video(
        src="demo.mp4",
        class_name="hero-video",
        title="Demo",
        controls=True,
    )

    html = render(video)

    assert 'src="demo.mp4"' in html
    assert 'class="hero-video"' in html
    assert 'title="Demo"' in html
    assert "controls" in html
