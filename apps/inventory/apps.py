# apps/inventory/apps.py
from django.apps import AppConfig

class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.inventory"   # <- IMPORTANTÍSIMO: ruta completa del paquete
    label = "inventory"       # (opcional) el app label para "makemigrations inventory"
    verbose_name = "Inventory"
