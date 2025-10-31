from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"   # ruta del paquete
    label = "core"       # <--- ESTE es el app_label que debes usar en FKs
