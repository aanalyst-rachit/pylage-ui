import pylage as ps
from pylage.core.registry import registry


DYNAMIC_COMPONENTS = [
    "Card",
    "Badge",
    "Avatar",
    "Accordion",
    "Carousel",
    "Image",
    "Video",
    "Audio",
    "Icon",
    "Canvas",
]


def test_all_dynamic_components_are_central_registry_components():
    for name in DYNAMIC_COMPONENTS:
        assert registry.has(name), f"{name} must exist in central registry"


def test_dynamic_components_do_not_need_factory_registration():
    for name in DYNAMIC_COMPONENTS:
        factory = getattr(ps, name)
        component = factory()
        assert component.type == name
        assert registry.has(component.type)


def test_central_registry_contains_unique_component_types():
    types = registry.types()
    assert len(types) == len(set(types))


def test_public_components_are_registry_backed():
    public_names = [
        "Card",
        "Badge",
        "Avatar",
        "Accordion",
        "Carousel",
        "Image",
        "Video",
        "Audio",
        "Icon",
        "Canvas",
    ]

    for name in public_names:
        assert callable(getattr(ps, name))
        assert registry.has(name)
