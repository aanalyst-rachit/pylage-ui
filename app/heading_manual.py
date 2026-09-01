import pylage as pl
from pylage import Style


def get_app():

    return pl.Column(

        pl.Heading(
            "Heading — Default",
        ),

        pl.Heading(
            "Heading — Large",
            style=Style(
                font_size="2.5rem",
                font_weight="700",
                color="#0f172a",
            ),
        ),

        pl.Heading(
            "Heading — Medium",
            style=Style(
                font_size="2rem",
                font_weight="600",
                color="#1e293b",
            ),
        ),

        pl.Heading(
            "Heading — Small",
            style=Style(
                font_size="1.5rem",
                font_weight="600",
                color="#334155",
            ),
        ),

        pl.Heading(
            "Heading — Custom Font",
            style=Style(
                font_size="2rem",
                font_family="Arial",
                font_weight="700",
                color="#2563eb",
            ),
        ),

        pl.Heading(
            "Heading — Center",
            style=Style(
                font_size="2rem",
                font_weight="700",
                text_align="center",
                color="#7c3aed",
                padding="1rem",
                background_color="#f5f3ff",
            ),
        ),

        pl.Heading(
            "Heading — With Spacing",
            style=Style(
                font_size="1.75rem",
                font_weight="700",
                margin="2rem",
                padding="1rem",
                color="#047857",
                background_color="#ecfdf5",
                border="1px solid #a7f3d0",
                border_radius="0.5rem",
            ),
        ),

        pl.Heading(
            "Heading — Full Width",
            style=Style(
                width="100%",
                font_size="2rem",
                font_weight="700",
                text_align="center",
                padding="1rem",
                background_color="#eff6ff",
                color="#1d4ed8",
                box_sizing="border-box",
            ),
        ),

        pl.Heading(
            "Heading — Line Height",
            style=Style(
                font_size="2rem",
                font_weight="700",
                line_height="1.5",
                color="#be123c",
            ),
        ),

        pl.Heading(
            "Heading — Shadow",
            style=Style(
                font_size="2rem",
                font_weight="700",
                color="#111827",
                box_shadow="0 2px 6px rgba(0,0,0,0.15)",
                padding="1rem",
            ),
        ),

        style=Style(
            width="100%",
            min_height="100vh",
            padding="2rem",
            gap="1rem",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    )
