from pylage_layout.layouts.navbar import Navbar
from pylage_layout.layouts.topbar import Topbar
from pylage_layout.layouts.header import Header
from pylage_layout.layouts.footer import Footer
from pylage_layout.layouts.drawer import NavigationDrawer, MobileSidebar
from pylage import ResponsiveStyle, Style


def test_phase_7e_responsive_assertion():
    responsive = ResponsiveStyle(
        base=Style(width="100%", flex_direction="column"),
        md=Style(flex_direction="row"),
        lg=Style(gap="2rem"),
    )

    components = [
        ("Navbar", Navbar),
        ("Topbar", Topbar),
        ("Header", Header),
        ("Footer", Footer),
        ("NavigationDrawer", NavigationDrawer),
        ("MobileSidebar", MobileSidebar),
    ]

    print("=" * 70)
    print("7E — FINAL RESPONSIVE ASSERTION CHECK")
    print("=" * 70)

    for name, factory in components:
        print(f"\n--- {name} ---")

        c = factory(style=responsive)

        assert c.props.get("style") is responsive, (
            f"{name}: style was not passed through"
        )

        assert c.props["style"].base.width == "100%", (
            f"{name}: base width failed"
        )

        assert c.props["style"].base.flex_direction == "column", (
            f"{name}: base flex_direction failed"
        )

        assert c.props["style"].md.flex_direction == "row", (
            f"{name}: md flex_direction failed"
        )

        assert c.props["style"].lg.gap == "2rem", (
            f"{name}: lg gap failed"
        )

        print("type :", c.type)
        print("PASS : style + base + md + lg")

    print("\n" + "=" * 70)
    print("7E FINAL RESULT: PASS")
    print("=" * 70)


if __name__ == "__main__":
    test_phase_7e_responsive_assertion()
