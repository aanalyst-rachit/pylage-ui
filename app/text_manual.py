import pylage as pl
from pylage import Style


def get_app():

    return pl.Column(

        # =========================================================
        # TEXT — BASIC
        # =========================================================
        pl.Text(
            "TEXT — Basic",
            style=Style(
                font_size="28px",
                font_weight="700",
                color="#0f172a",
                margin_bottom="10px",
            ),
        ),

        pl.Text(
            "This is a normal Text component.",
            style=Style(
                color="#334155",
                font_size="16px",
            ),
        ),

        # =========================================================
        # FONT SIZE
        # =========================================================
        pl.Text(
            "Font Size: 12px",
            style=Style(
                font_size="12px",
                color="#475569",
            ),
        ),

        pl.Text(
            "Font Size: 20px",
            style=Style(
                font_size="20px",
                color="#475569",
            ),
        ),

        pl.Text(
            "Font Size: 32px",
            style=Style(
                font_size="32px",
                color="#475569",
            ),
        ),

        # =========================================================
        # FONT WEIGHT
        # =========================================================
        pl.Text(
            "Font Weight: 400 — Normal",
            style=Style(
                font_weight="400",
                font_size="18px",
            ),
        ),

        pl.Text(
            "Font Weight: 600 — Semi Bold",
            style=Style(
                font_weight="600",
                font_size="18px",
            ),
        ),

        pl.Text(
            "Font Weight: 700 — Bold",
            style=Style(
                font_weight="700",
                font_size="18px",
            ),
        ),

        # =========================================================
        # FONT FAMILY
        # =========================================================
        pl.Text(
            "Font Family: Arial",
            style=Style(
                font_family="Arial",
                font_size="20px",
            ),
        ),

        pl.Text(
            "Font Family: Georgia",
            style=Style(
                font_family="Georgia",
                font_size="20px",
            ),
        ),

        pl.Text(
            "Font Family: monospace",
            style=Style(
                font_family="monospace",
                font_size="20px",
            ),
        ),

        # =========================================================
        # COLOR
        # =========================================================
        pl.Text(
            "Text Color",
            style=Style(
                color="#2563eb",
                font_size="22px",
                font_weight="700",
            ),
        ),

        pl.Text(
            "Different Text Color",
            style=Style(
                color="#dc2626",
                font_size="22px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BACKGROUND
        # =========================================================
        pl.Text(
            "Text with Background",
            style=Style(
                background_color="#dbeafe",
                color="#1e40af",
                padding="10px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # TEXT ALIGN
        # =========================================================
        pl.Text(
            "Left Aligned Text",
            style=Style(
                width="100%",
                text_align="left",
                font_size="18px",
            ),
        ),

        pl.Text(
            "Center Aligned Text",
            style=Style(
                width="100%",
                text_align="center",
                font_size="18px",
            ),
        ),

        pl.Text(
            "Right Aligned Text",
            style=Style(
                width="100%",
                text_align="right",
                font_size="18px",
            ),
        ),

        # =========================================================
        # LINE HEIGHT
        # =========================================================
        pl.Text(
            "Line Height Demo — This is a longer piece of text "
            "so that we can visually inspect how line-height "
            "changes the spacing between lines.",
            style=Style(
                width="500px",
                font_size="18px",
                line_height="2",
            ),
        ),

        # =========================================================
        # PADDING
        # =========================================================
        pl.Text(
            "Text with Padding",
            style=Style(
                background_color="#fef3c7",
                color="#92400e",
                padding="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # MARGIN
        # =========================================================
        pl.Text(
            "Text with Margin",
            style=Style(
                background_color="#dcfce7",
                color="#166534",
                padding="10px",
                margin="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BORDER
        # =========================================================
        pl.Text(
            "Text with Border",
            style=Style(
                border="1px solid #94a3b8",
                padding="12px",
                border_radius="8px",
                color="#0f172a",
            ),
        ),

        # =========================================================
        # BORDER RADIUS
        # =========================================================
        pl.Text(
            "Rounded Text Box",
            style=Style(
                background_color="#ede9fe",
                color="#5b21b6",
                padding="12px 20px",
                border_radius="20px",
                font_weight="700",
            ),
        ),

        # =========================================================
        # BOX SHADOW
        # =========================================================
        pl.Text(
            "Text Box with Shadow",
            style=Style(
                background_color="#ffffff",
                color="#0f172a",
                padding="15px",
                border_radius="8px",
                box_shadow="0 4px 10px rgba(0,0,0,0.15)",
            ),
        ),

        # =========================================================
        # OPACITY
        # =========================================================
        pl.Text(
            "Opacity 100%",
            style=Style(
                opacity=1,
                font_size="18px",
            ),
        ),

        pl.Text(
            "Opacity 50%",
            style=Style(
                opacity=0.5,
                font_size="18px",
            ),
        ),

        # =========================================================
        # WIDTH
        # =========================================================
        pl.Text(
            "Fixed Width Text",
            style=Style(
                width="300px",
                background_color="#e0f2fe",
                padding="10px",
            ),
        ),

        # =========================================================
        # OVERFLOW
        # =========================================================
        pl.Text(
            "Overflow demonstration — this is intentionally a "
            "very long text string to inspect overflow behaviour.",
            style=Style(
                width="250px",
                overflow="hidden",
                background_color="#f1f5f9",
                padding="10px",
            ),
        ),

        # =========================================================
        # CURSOR
        # =========================================================
        pl.Text(
            "Cursor: pointer",
            style=Style(
                cursor="pointer",
                color="#2563eb",
                font_weight="700",
            ),
        ),

        # =========================================================
        # COMBINED REAL-WORLD TEXT
        # =========================================================
        pl.Text(
            "Dashboard Title",
            style=Style(
                font_size="30px",
                font_weight="700",
                font_family="Arial",
                color="#0f172a",
                margin_bottom="8px",
            ),
        ),

        pl.Text(
            "Manage your application, users and analytics "
            "from one place.",
            style=Style(
                font_size="16px",
                font_weight="400",
                color="#64748b",
                line_height="1.6",
                max_width="600px",
            ),
        ),

        style=Style(
            width="100%",
            min_height="100vh",
            padding="30px",
            background_color="#f8fafc",
            color="#0f172a",
            display="flex",
            flex_direction="column",
            gap="16px",
            box_sizing="border-box",
        ),
    )
