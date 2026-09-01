import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps
from pylage import Style

def get_app():
    # State tracking for interactive canvas/media status
    media_status = ps.State("Status: Media components ready")

    def handle_media_click():
        media_status.set("⚡ Media component clicked!")

    # ============================================================
    # 1. IMAGE COMPONENT
    # ============================================================
    image_section = ps.Column(
        ps.Text("1. Image Component", style=Style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        ps.Image(
            src="https://picsum.photos/600/200",
            alt="Sample Placeholder Image",
            style=Style(
                width="100%",
                height="150px",
                border_radius="0.5rem",
                border="1px solid #cbd5e1",
            ),
        ),
    )

    # ============================================================
    # 2. VIDEO COMPONENT
    # ============================================================
    video_section = ps.Column(
        ps.Text("2. Video Component", style=Style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        ps.Video(
            src="https://www.w3schools.com/html/mov_bbb.mp4",
            controls=True,
            style=Style(
                width="100%",
                max_height="220px",
                border_radius="0.5rem",
                background_color="#000000",
            ),
        ),
    )

    # ============================================================
    # 3. AUDIO COMPONENT
    # ============================================================
    audio_section = ps.Column(
        ps.Text("3. Audio Component", style=Style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        ps.Audio(
            src="https://www.w3schools.com/html/horse.mp3",
            controls=True,
            style=Style(width="100%"),
        ),
    )

    # ============================================================
    # 4. ICON & AVATAR (HORIZONTAL DIVIDER DEMO)
    # ============================================================
    icon_avatar_section = ps.Column(
        ps.Text("4. Icon & Avatar (Side-by-Side with Vertical Divider)", style=Style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        ps.Row(
            # Icon Demo (Fixed: Using name="...")
            ps.Column(
                ps.Text("Icons", style=Style(font_weight="600", font_size="0.9rem", margin_bottom="0.25rem")),
                ps.Row(
                    ps.Icon(name="check", style=Style(color="#166534", font_size="1.5rem")),
                    ps.Icon(name="star", style=Style(color="#d97706", font_size="1.5rem")),
                    ps.Icon(name="user", style=Style(color="#2563eb", font_size="1.5rem")),
                    style=Style(gap="0.75rem", align_items="center"),
                ),
            ),
            
            # VERTICAL DIVIDER
            ps.Divider(
                orientation="vertical",
                style=Style(height="50px", border="1px solid #cbd5e1", margin="0 1rem"),
            ),
            
            # Avatar Demo
            ps.Column(
                ps.Text("Avatars", style=Style(font_weight="600", font_size="0.9rem", margin_bottom="0.25rem")),
                ps.Row(
                    ps.Avatar(
                        src="https://i.pravatar.cc/100?img=33",
                        name="Rachit Kumar",
                        style=Style(width="40px", height="40px", border_radius="999px"),
                    ),
                    ps.Avatar(
                        name="User Fallback",
                        style=Style(width="40px", height="40px", border_radius="999px", background_color="#2563eb", color="#ffffff"),
                    ),
                    style=Style(gap="0.75rem", align_items="center"),
                ),
            ),
            style=Style(align_items="center", padding="1rem", background_color="#ffffff", border="1px solid #e2e8f0", border_radius="0.5rem"),
        ),
    )

    # ============================================================
    # 5. CANVAS COMPONENT
    # ============================================================
    canvas_section = ps.Column(
        ps.Text("5. Canvas Component (Interactive Render)", style=Style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        ps.Canvas(
            width=500,
            height=120,
            on_click=handle_media_click,
            style=Style(
                width="100%",
                height="120px",
                background_color="#f1f5f9",
                border="1px dashed #2563eb",
                border_radius="0.5rem",
                cursor="pointer",
            ),
        ),
    )

    # Horizontal Divider Helper
    def create_horizontal_divider():
        return ps.Divider(
            orientation="horizontal",
            style=Style(
                width="100%",
                border="1px solid #e2e8f0",
                margin="1.5rem 0",
            ),
        )

    # ============================================================
    # MAIN APP STRUCTURE
    # ============================================================
    return ps.Column(
        ps.Heading(
            "PyLage Media — Live Manual",
            style=Style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        ps.Text(
            "Media components (Image, Video, Audio, Icon, Canvas, Avatar) with Horizontal & Vertical Dividers:",
            style=Style(color="#64748b", margin_bottom="1rem"),
        ),

        ps.Text(media_status, style=Style(color="#166534", font_weight="600", margin_bottom="1rem")),

        image_section,
        create_horizontal_divider(),

        video_section,
        create_horizontal_divider(),

        audio_section,
        create_horizontal_divider(),

        icon_avatar_section,
        create_horizontal_divider(),

        canvas_section,

        style=Style(
            width="100%",
            max_width="750px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )