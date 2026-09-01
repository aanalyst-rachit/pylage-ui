import pylage as pl
from pylage import Style

from pylage_layout.layouts import AppShell, Container, TwoColumn, Footer
from pylage_layout.patterns import (
    Hero,
    FeatureSection,
    CTA,
    StatsSection,
    PricingSection,
    ContentSection,
)


# ============================================================
# 1. Global page style (Light Theme)
# ============================================================

page_style = Style(
    width="100%",
    min_height="100vh",
    background_color="#f8fafc",  # Light slate background
    color="#0f172a",             # Dark slate text
    box_sizing="border-box",
)


# ============================================================
# 2. Header
# ============================================================

header = pl.Row(
    pl.Text(
        "PyLage Dashboard",
        style=Style(
            font_size="1.35rem",
            font_weight="700",
            color="#0f172a",
        ),
    ),
    pl.Card(
        "Admin Console",
        style=Style(
            font_size="0.9rem",
            color="#64748b",
        ),
    ),
    style=Style(
        width="100%",
        display="flex",
        flex_direction="row",
        justify_content="space-between",
        align_items="center",
        padding="1.25rem 2rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 3. Sidebar
# ============================================================

sidebar = pl.Column(
    pl.Text(
        "NAVIGATION",
        style=Style(
            font_size="0.75rem",
            font_weight="700",
            color="#94a3b8",
            margin_bottom="1rem",
        ),
    ),

    pl.Text(
        "▣  Dashboard",
        style=Style(
            padding="0.75rem",
            background_color="#eff6ff",
            color="#1d4ed8",
            border="1px solid #bfdbfe",
            border_radius="0.5rem",
            font_weight="600",
            margin_bottom="0.5rem",
        ),
    ),

    pl.Text(
        "▤  Analytics",
        style=Style(
            padding="0.75rem",
            color="#475569",
            margin_bottom="0.5rem",
        ),
    ),

    pl.Text(
        "◉  Customers",
        style=Style(
            padding="0.75rem",
            color="#475569",
            margin_bottom="0.5rem",
        ),
    ),

    pl.Text(
        "⚙  Settings",
        style=Style(
            padding="0.75rem",
            color="#475569",
        ),
    ),

    style=Style(
        width="260px",
        min_width="260px",
        padding="1.5rem",
        background_color="#ffffff",
        color="#334155",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 4. Hero
# ============================================================

def on_get_started():
    print("GET STARTED CLICKED")


def on_view_documentation():
    print("VIEW DOCUMENTATION CLICKED")


hero = Hero(
    title="Build dashboards without fighting layout",

    description=(
        "A responsive dashboard composed entirely from "
        "reusable pylage_layout primitives and patterns."
    ),

    actions=[
        pl.Text(
            "Get Started",
            style=Style(
                padding="0.6rem 1.2rem",
                background_color="#2563eb",
                color="#ffffff",
                border_radius="0.375rem",
                font_weight="600",
                margin_right="0.75rem",
            ),
        ).on("click", on_get_started),

        pl.Text(
            "View Documentation",
            style=Style(
                padding="0.6rem 1.2rem",
                background_color="#ffffff",
                color="#1e293b",
                border="1px solid #cbd5e1",
                border_radius="0.375rem",
                font_weight="600",
            ),
        ).on("click", on_view_documentation),
    ],

    style=Style(
        width="100%",
        padding="2rem",
        background_color="#eff6ff",
        color="#1e3a8a",
        border="1px solid #bfdbfe",
        border_radius="0.75rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        box_sizing="border-box",
    ),
)


# ============================================================
# 5. Statistics
# ============================================================

stats = StatsSection(
    title="Overview",

    description="Current application metrics",

    stats=[
        {
            "value": "12.8K",
            "label": "Total Users",
            "description": "+18.4% this month",
        },
        {
            "value": "8.42K",
            "label": "Active Users",
            "description": "+12.7% this month",
        },
        {
            "value": "$48.2K",
            "label": "Revenue",
            "description": "+24.1% this month",
        },
        {
            "value": "94.8%",
            "label": "Conversion",
            "description": "+4.2% this month",
        },
    ],

    style=Style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 6. Feature section
# ============================================================

features = FeatureSection(
    {
        "title": "Design Tokens",
        "description": (
            "Consistent spacing, colors, typography and radius."
        ),
    },

    {
        "title": "Responsive Layout",
        "description": (
            "Mobile-first layouts using ResponsiveStyle."
        ),
    },

    {
        "title": "Reusable Patterns",
        "description": (
            "Build complex pages from small compositions."
        ),
    },

    {
        "title": "Theme Ready",
        "description": (
            "Design systems can be connected to reusable themes."
        ),
    },

    title="Why pylage_layout?",

    description=(
        "Everything is composed from reusable building blocks."
    ),

    style=Style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 7. Analytics
# ============================================================

analytics = ContentSection(
    title="Analytics",

    content=(
        "Your application is growing steadily. "
        "Revenue and active users are both trending upward."
    ),

    actions=[
        pl.Text(
            "Revenue ↑ 24.1%",
            style=Style(
                padding="0.75rem 1rem",
                background_color="#dcfce7",
                color="#166534",
                border="1px solid #bbf7d0",
                border_radius="0.5rem",
                margin_right="0.75rem",
            ),
        ),

        pl.Text(
            "Users ↑ 18.4%",
            style=Style(
                padding="0.75rem 1rem",
                background_color="#dbeafe",
                color="#1e40af",
                border="1px solid #bfdbfe",
                border_radius="0.5rem",
            ),
        ),
    ],

    style=Style(
        width="100%",
        padding="2rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 8. Pricing
# ============================================================

pricing = PricingSection(
    title="Plans",

    description="Choose the plan that fits your team.",

    plans=[
        {
            "name": "Starter",
            "price": "$9",
            "description": "For individuals.",
            "features": [
                "1 project",
                "Basic analytics",
                "Community support",
            ],
            "action": "Start Starter",
        },

        {
            "name": "Professional",
            "price": "$29",
            "description": "For growing teams.",
            "features": [
                "10 projects",
                "Advanced analytics",
                "Priority support",
            ],
            "action": "Choose Pro",
            "featured": True,
        },

        {
            "name": "Enterprise",
            "price": "$99",
            "description": "For larger organizations.",
            "features": [
                "Unlimited projects",
                "Advanced security",
                "Dedicated support",
            ],
            "action": "Contact Sales",
        },
    ],

    style=Style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 9. CTA
# ============================================================

cta = CTA(
    title="Ready to ship faster?",

    description=(
        "Compose responsive pages with PyLage Layout "
        "instead of rebuilding layouts from scratch."
    ),

    actions=[
        pl.Text(
            "Install Now",
            style=Style(
                padding="0.75rem 1.5rem",
                background_color="#4338ca",
                color="#ffffff",
                border_radius="0.5rem",
                font_weight="600",
                display="inline-block",
            ),
        ),
    ],

    style=Style(
        width="100%",
        padding="2rem",
        background_color="#eef2ff",
        color="#312e81",
        border="1px solid #c7d2fe",
        border_radius="0.75rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        box_sizing="border-box",
    ),
)


# ============================================================
# 10. Footer
# ============================================================

footer = Footer(
    pl.Text(
        "PyLage Layout • Responsive UI composition for Python",
        style=Style(
            color="#64748b",
            font_size="0.85rem",
        ),
    ),

    style=Style(
        width="100%",
        padding="1.5rem 2rem",
        background_color="#ffffff",
        color="#64748b",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 11. Dashboard content
# ============================================================

dashboard_content = pl.Column(
    hero,
    stats,
    features,
    analytics,
    pricing,
    cta,
    footer,

    style=Style(
        width="100%",
        min_width="0",
        display="flex",
        flex_direction="column",
        gap="1.5rem",
        padding="1.5rem",
        background_color="#f8fafc",
        color="#0f172a",
        box_sizing="border-box",
    ),
)


# ============================================================
# 12. Main two-column layout
# ============================================================

columns = TwoColumn(
    sidebar,

    Container(
        dashboard_content,

        style=Style(
            width="100%",
            min_width="0",
            max_width="100%",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    ),

    style=Style(
        width="100%",
        display="flex",
        flex_direction="row",
        gap="0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 13. Application shell
# ============================================================

app = AppShell(
    header=header,
    content=columns,
    style=page_style,
)


# ============================================================
# 14. Run
# ============================================================

def get_app():
    return app