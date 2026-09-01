from pylage import Skeleton
from pylage.core.renderer import render


def test_skeleton_renders_as_div():
    skeleton = Skeleton()

    html = render(skeleton)

    assert "<div" in html


def test_skeleton_supports_props():
    skeleton = Skeleton(
        class_name="loading-skeleton",
        title="Loading content",
    )

    html = render(skeleton)

    assert 'class="loading-skeleton"' in html
    assert 'title="Loading content"' in html


def test_skeleton_supports_text():
    skeleton = Skeleton(
        text="Loading...",
    )

    html = render(skeleton)

    assert "Loading..." in html
