from django.apps import AppConfig


class DjangoPlausibleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plausible_proxy"
    verbose_name = "Plausible Proxy"
