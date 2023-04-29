from django.apps import AppConfig


class SubmanageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "submanage"

    def ready(self):
        import submanage.signals
