from pylage import Image
from pylage.core.renderer import render


def test_image_creates_image_component():
    image = Image()

    assert image.type == "Image"


def test_image_renders_as_img():
    image = Image(
        src="photo.jpg",
        alt="A photo",
    )

    html = render(image)

    assert "<img" in html
    assert 'src="photo.jpg"' in html
    assert 'alt="A photo"' in html


def test_image_supports_props():
    image = Image(
        src="avatar.png",
        alt="Avatar",
        class_name="profile-image",
        title="Profile",
    )

    html = render(image)

    assert 'src="avatar.png"' in html
    assert 'alt="Avatar"' in html
    assert 'class="profile-image"' in html
    assert 'title="Profile"' in html
