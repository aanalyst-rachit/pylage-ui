from pylage import Audio
from pylage.core.renderer import render


def test_audio_creates_audio_component():
    audio = Audio()

    assert audio.type == "Audio"


def test_audio_renders_as_audio():
    audio = Audio(
        src="song.mp3",
        controls=True,
    )

    html = render(audio)

    assert "<audio" in html
    assert 'src="song.mp3"' in html
    assert "controls" in html
    assert "</audio>" in html


def test_audio_supports_props():
    audio = Audio(
        src="track.mp3",
        class_name="player",
        title="Music",
        controls=True,
    )

    html = render(audio)

    assert 'src="track.mp3"' in html
    assert 'class="player"' in html
    assert 'title="Music"' in html
    assert "controls" in html
