from typing import Any, Dict
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from .models import Organization, Company, AnalystCompany
from .selectors import get_allowed_company_ids

User = get_user_model()


class CompanyScopedAdmin(admin.ModelAdmin):
    """Limita el queryset por empresas permitidas para el usuario."""
    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed = get_allowed_company_ids(request.user)
        return qs.filter(id__in=allowed)

    def has_view_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.id in get_allowed_company_ids(request.user)

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.id in get_allowed_company_ids(request.user)

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.id in get_allowed_company_ids(request.user)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "tax_id", "created_at")
    search_fields = ("name", "tax_id")


@admin.register(Company)
class CompanyAdmin(CompanyScopedAdmin):
    list_display = (
        "name", "tax_id", "municipality", "org_type",
        "advisor", "assessment_date", "created_at",
    )
    search_fields = (
        "name", "tax_id", "municipality",
        "contact_name", "contact_email", "contact_phone",
    )
    list_filter = ("org_type", "municipality", "advisor")

    # Opción B: solo autocomplete para Organization; 'advisor' se limita al usuario actual.
    autocomplete_fields = ("organization",)

    # >>> Firma EXACTA que espera Django (HttpRequest, no opcional)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limita el campo 'advisor' al usuario autenticado cuando NO es superuser
        y lo preselecciona.
        """
        if db_field.name == "advisor" and request and request.user.is_authenticated and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(pk=request.user.pk)
            kwargs.setdefault("initial", request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # >>> También con firma exacta y tipo de retorno explícito
    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Inicial por defecto para 'advisor' en el formulario de 'Añadir'.
        """
        data: Dict[str, Any] = super().get_changeform_initial_data(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            data.setdefault("advisor", request.user.pk)
        return data

    def save_model(self, request: HttpRequest, obj: Company, form, change: bool):
        """
        Garantiza que 'advisor' quede asignado al usuario actual si vino vacío.
        """
        if not obj.advisor and not request.user.is_superuser:
            obj.advisor = request.user
        super().save_model(request, obj, form, change)


@admin.register(AnalystCompany)
class AnalystCompanyAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "assigned_at")
    search_fields = ("user__username", "company__name")
