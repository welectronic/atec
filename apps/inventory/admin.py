# apps/inventory/admin.py
from django.contrib import admin
from . import models


# ---------- Inlines ----------
class EquipmentMaintenanceInline(admin.TabularInline):
    model = models.EquipmentMaintenance
    extra = 1
    fields = ("maintenance_type", "frequency", "last_date", "notes")
    show_change_link = True


class EquipmentEnergyInline(admin.TabularInline):
    model = models.EquipmentEnergy
    extra = 1
    autocomplete_fields = ("energy_source",)
    fields = ("energy_source", "notes")
    show_change_link = True


# ---------- Admins ----------
@admin.register(models.EnergySource)
class EnergySourceAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(models.Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    inlines = (EquipmentMaintenanceInline, EquipmentEnergyInline)
    list_display = (
        "name", "company", "category",
        "purchase_year", "utilization_pct",
    )
    list_filter = ("category", "purchase_year")
    search_fields = ("name", "description")
    # Usa raw_id para evitar cargar todas las empresas en un select grande
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    # Orden por defecto
    ordering = ("name",)


@admin.register(models.TechnicalService)
class TechnicalServiceAdmin(admin.ModelAdmin):
    list_display = ("company", "service_type", "provider_name", "service_location")
    list_filter = ("service_type", "service_location")
    search_fields = ("provider_name", "service_description")
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.PlantLayout)
class PlantLayoutAdmin(admin.ModelAdmin):
    list_display = ("company", "layout_type")
    list_filter = ("layout_type",)
    search_fields = ("description",)
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.WorkMethod)
class WorkMethodAdmin(admin.ModelAdmin):
    list_display = ("company", "modality", "shifts_count")
    list_filter = ("modality",)
    search_fields = ("description", "shift_pattern")
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.SoftwareAsset)
class SoftwareAssetAdmin(admin.ModelAdmin):
    list_display = ("company", "name", "usage", "area")
    list_filter = ("usage", "area")
    search_fields = ("name", "description")
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("company", "name", "category", "origin", "inventory_management", "cost_share_pct")
    list_filter = ("category", "origin", "inventory_management")
    search_fields = ("name",)
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(models.Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "company", "item_name", "category", "motive", "amount_cop",
        "funding_source", "status", "investment_date", "investment_year",
        "equipment",
    )
    list_filter = ("category", "motive", "funding_source", "status")
    search_fields = ("item_name", "funding_entity", "notes")
    date_hierarchy = "investment_date"
    raw_id_fields = ("company", "equipment")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-investment_date", "-investment_year")


@admin.register(models.WorkforceProfile)
class WorkforceProfileAdmin(admin.ModelAdmin):
    list_display = ("company", "area", "people_count", "education_level", "avg_experience_years")
    list_filter = ("education_level", "area")
    search_fields = ("area",)
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("company", "area")


@admin.register(models.DisciplineAssessment)
class DisciplineAssessmentAdmin(admin.ModelAdmin):
    list_display = ("company", "item", "importance_score", "adoption_level")
    list_filter = ("importance_score", "adoption_level")
    search_fields = ("item", "notes")
    raw_id_fields = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("company", "item")


# Para que el through se pueda ver/editar directo si lo necesitas (además del inline)
@admin.register(models.EquipmentEnergy)
class EquipmentEnergyAdmin(admin.ModelAdmin):
    list_display = ("equipment", "energy_source", "notes")
    search_fields = ("equipment__name", "energy_source__name", "notes")
    raw_id_fields = ("equipment", "energy_source")
    readonly_fields = ("created_at", "updated_at")
