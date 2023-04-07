from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ThemesDefaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "themes.default"
    label = "themes_default"

    def ready(self):
        post_migrate.connect(init_app, sender=self)
        return super().ready()


def init_app(sender, **kwargs):
    """Create initial main navigation menu"""
    pass
