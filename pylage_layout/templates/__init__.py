"""Public page templates."""

from .landing import LandingPage
from .dashboard import Dashboard
from .admin import AdminPanel
from .authentication import Authentication
from .profile import ProfilePage

__all__ = [
    "LandingPage",
    "Dashboard",
    "AdminPanel",
    "Authentication",
    "ProfilePage",
]

from .admin import AdminPanel
from .settings import Settings, SettingsPage
