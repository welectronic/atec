# apps/inventory/urls.py
from django.urls import path
from .views import (
    InventoryManageView,
    equipment_list,
    equipment_create,
    equipment_update,
    equipment_delete,
    service_list,
    service_create,
    service_update,
    service_delete,
    maintenance_list,
    maintenance_create,
    maintenance_update,
    maintenance_delete,
    # New endpoints
    method_list,
    method_create,
    method_update,
    method_delete,
    layout_list,
    layout_create,
    layout_update,
    layout_delete,
    software_list,
    software_create,
    software_update,
    software_delete,
    material_list,
    material_create,
    material_update,
    material_delete,
    investment_list,
    investment_create,
    investment_update,
    investment_delete,
    workforce_list,
    workforce_create,
    workforce_update,
    workforce_delete,
    discipline_list,
    discipline_create,
    discipline_update,
    discipline_delete,
)

app_name = "inventory"

urlpatterns = [
    path("manage/<int:company_id>/", InventoryManageView.as_view(), name="manage"),
    # HTMX endpoints para Equipos
    path("equipment/<int:company_id>/list/", equipment_list, name="equipment_list"),
    path("equipment/<int:company_id>/new/", equipment_create, name="equipment_create"),
    path("equipment/<int:pk>/edit/", equipment_update, name="equipment_update"),
    path("equipment/<int:pk>/delete/", equipment_delete, name="equipment_delete"),
    # --- Servicios técnicos (HTMX) ---
    path("services/<int:company_id>/list/", service_list, name="service_list"),
    path("services/<int:company_id>/new/", service_create, name="service_create"),
    path("services/<int:pk>/edit/", service_update, name="service_update"),
    path("services/<int:pk>/delete/", service_delete, name="service_delete"),

    path("maintenance/<int:company_id>/list/", maintenance_list, name="maintenance_list"),
    path("maintenance/<int:company_id>/new/", maintenance_create, name="maintenance_create"),
    path("maintenance/<int:pk>/edit/", maintenance_update, name="maintenance_update"),
    path("maintenance/<int:pk>/delete/", maintenance_delete, name="maintenance_delete"),

    # --- Métodos de trabajo (HTMX) ---
    path("methods/<int:company_id>/list/", method_list, name="method_list"),
    path("methods/<int:company_id>/new/", method_create, name="method_create"),
    path("methods/<int:pk>/edit/", method_update, name="method_update"),
    path("methods/<int:pk>/delete/", method_delete, name="method_delete"),

    # --- Layout (HTMX) ---
    path("layout/<int:company_id>/list/", layout_list, name="layout_list"),
    path("layout/<int:company_id>/new/", layout_create, name="layout_create"),
    path("layout/<int:pk>/edit/", layout_update, name="layout_update"),
    path("layout/<int:pk>/delete/", layout_delete, name="layout_delete"),

    # --- Software (HTMX) ---
    path("software/<int:company_id>/list/", software_list, name="software_list"),
    path("software/<int:company_id>/new/", software_create, name="software_create"),
    path("software/<int:pk>/edit/", software_update, name="software_update"),
    path("software/<int:pk>/delete/", software_delete, name="software_delete"),

    # --- Materiales (HTMX) ---
    path("materials/<int:company_id>/list/", material_list, name="material_list"),
    path("materials/<int:company_id>/new/", material_create, name="material_create"),
    path("materials/<int:pk>/edit/", material_update, name="material_update"),
    path("materials/<int:pk>/delete/", material_delete, name="material_delete"),

    # --- Inversiones (HTMX) ---
    path("investments/<int:company_id>/list/", investment_list, name="investment_list"),
    path("investments/<int:company_id>/new/", investment_create, name="investment_create"),
    path("investments/<int:pk>/edit/", investment_update, name="investment_update"),
    path("investments/<int:pk>/delete/", investment_delete, name="investment_delete"),

    # --- Talento (HTMX) ---
    path("workforce/<int:company_id>/list/", workforce_list, name="workforce_list"),
    path("workforce/<int:company_id>/new/", workforce_create, name="workforce_create"),
    path("workforce/<int:pk>/edit/", workforce_update, name="workforce_update"),
    path("workforce/<int:pk>/delete/", workforce_delete, name="workforce_delete"),

    # --- Disciplinas (HTMX) ---
    path("disciplines/<int:company_id>/list/", discipline_list, name="discipline_list"),
    path("disciplines/<int:company_id>/new/", discipline_create, name="discipline_create"),
    path("disciplines/<int:pk>/edit/", discipline_update, name="discipline_update"),
    path("disciplines/<int:pk>/delete/", discipline_delete, name="discipline_delete"),

]
