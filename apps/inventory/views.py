# apps/inventory/views.py
from __future__ import annotations

import json
from functools import wraps
from typing import Callable, Tuple

from django.conf import settings
from django.apps import apps as django_apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from .models import (
    Equipment,
    TechnicalService,
    EquipmentMaintenance,
    WorkMethod,
    PlantLayout,
    SoftwareAsset,
    DisciplineAssessment,
    WorkforceProfile,
    Material,
    Investment,
)
from .forms import (
    EquipmentForm,
    TechnicalServiceForm,
    MaintenanceForm,
    WorkMethodForm,
    PlantLayoutForm,
    SoftwareAssetForm,
    DisciplineAssessmentForm,
    WorkforceProfileForm,
    MaterialForm,
    InvestmentForm,
)

# Resolver Company dinámicamente
COMPANY_MODEL = getattr(settings, "COMPANY_MODEL", "core.Company")
app_label, model_name = COMPANY_MODEL.rsplit(".", 1)
Company = django_apps.get_model(app_label, model_name)

# Tabs visibles en la UI
TABS = [
    ("equipment", "Equipos"),
    ("maintenance", "Mantenimiento"),
    ("services", "Servicios técnicos"),
    ("methods", "Métodos"),
    ("layout", "Layout"),
    ("software", "Software"),
    ("materials", "Materiales"),
    ("investments", "Inversiones"),
    ("workforce", "Talento"),
    ("disciplines", "Saberes/Disciplinas"),
    ("summary", "Resumen & Validación"),
]


class InventoryManageView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/manage.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, id=kwargs["company_id"])
        current_tab = self.request.GET.get("tab", "equipment")
        valid = {s for s, _ in TABS}
        if current_tab not in valid:
            current_tab = "equipment"
        ctx.update(
            company=company,
            tabs=TABS,
            current_tab=current_tab,
            partial=f"inventory/tabs/_{current_tab}.html",
            page_title=f"Inventario tecnológico — {company.name}",  # type: ignore
        )
        return ctx

    def get(self, request: HttpRequest, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        is_hx = request.headers.get("HX-Request") == "true" or request.META.get("HTTP_HX_REQUEST") == "true"
        if is_hx:
            # Solo el contenido del tab
            return render(request, ctx["partial"], ctx)
        # Página completa
        return render(request, self.template_name, ctx)


# ---------------- Utilidades HTMX ----------------

def _hx_trigger(event_name: str, close_modal: bool = True) -> HttpResponse:
    """
    204 con cabecera HX-Trigger. Emite el evento que refresca la tabla
    y opcionalmente una señal para cerrar el modal.
    """
    payload = {event_name: True}
    if close_modal:
        payload["modal:close"] = True
    resp = HttpResponse(status=204)
    resp["HX-Trigger"] = json.dumps(payload)
    return resp


# ---------------- Factory CRUD HTMX ----------------

def crud_factory(
    *,
    model,
    form_class,
    list_template: str,
    form_template: str,
    event_name: str,
    qs_by_company: Callable,                # def(company) -> QuerySet
    company_from_obj: Callable,             # def(obj) -> Company
    before_create: Callable | None = None,  # def(obj, company, form) -> None
    form_kwargs_fn: Callable | None = None, # def(company, instance=None) -> dict
) -> Tuple:
    """
    Devuelve 4 FBVs: list_view, create_view, update_view, delete_view.
    Todas disparan HX-Trigger con `event_name` y cierran modal con `modal:close`.
    """

    def get_company(company_id: int):
        return get_object_or_404(Company, pk=company_id)

    def with_login(view):
        @login_required
        @wraps(view)
        def _wrapped(*args, **kwargs):
            return view(*args, **kwargs)
        return _wrapped

    @with_login
    @require_http_methods(["GET"])
    def list_view(request: HttpRequest, company_id: int) -> HttpResponse:
        company = get_company(company_id)
        qs = qs_by_company(company)
        ctx = {"company": company, "object_list": qs}
        return render(request, list_template, ctx)

    @with_login
    @csrf_protect
    @require_http_methods(["GET", "POST"])
    def create_view(request: HttpRequest, company_id: int) -> HttpResponse:
        company = get_company(company_id)
        kw = (form_kwargs_fn or (lambda c, instance=None: {}))(company, None)

        if request.method == "POST":
            form = form_class(request.POST, **kw)
            if form.is_valid():
                obj = form.save(commit=False)
                if before_create:
                    before_create(obj, company, form)
                obj.save()
                if hasattr(form, "save_m2m"):
                    form.save_m2m()
                return _hx_trigger(event_name, True)
        else:
            form = form_class(**kw)

        ctx = {
            "form": form,
            "company": company,
            "title": f"Agregar {model._meta.verbose_name}",
            "action": "create",
        }
        return render(request, form_template, ctx)

    @with_login
    @csrf_protect
    @require_http_methods(["GET", "POST"])
    def update_view(request: HttpRequest, pk: int) -> HttpResponse:
        obj = get_object_or_404(model, pk=pk)
        company = company_from_obj(obj)
        kw = (form_kwargs_fn or (lambda c, instance=None: {}))(company, obj)

        if request.method == "POST":
            form = form_class(request.POST, instance=obj, **kw)
            if form.is_valid():
                form.save()
                return _hx_trigger(event_name, True)
        else:
            form = form_class(instance=obj, **kw)

        ctx = {
            "form": form,
            "company": company,
            "title": f"Editar {model._meta.verbose_name}",
            "action": "update",
            "object": obj,
        }
        return render(request, form_template, ctx)

    @with_login
    @csrf_protect
    @require_http_methods(["POST", "DELETE"])
    def delete_view(request: HttpRequest, pk: int) -> HttpResponse:
        obj = get_object_or_404(model, pk=pk)
        obj.delete()
        return _hx_trigger(event_name, True)

    return list_view, create_view, update_view, delete_view


# ---------------- Equipos ----------------

equipment_list, equipment_create, equipment_update, equipment_delete = crud_factory(
    model=Equipment,
    form_class=EquipmentForm,
    list_template="inventory/equipment/_table.html",
    form_template="inventory/equipment/_form_modal.html",
    event_name="equipment:refresh",
    qs_by_company=lambda company: Equipment.objects.filter(company=company).order_by("name"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Servicios técnicos ----------------

service_list, service_create, service_update, service_delete = crud_factory(
    model=TechnicalService,
    form_class=TechnicalServiceForm,
    list_template="inventory/services/_table.html",
    form_template="inventory/services/_form_modal.html",
    event_name="services:refresh",
    qs_by_company=lambda company: TechnicalService.objects.filter(company=company).order_by(
        "service_type", "provider_name"
    ),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Mantenimiento de equipos ----------------

maintenance_list, maintenance_create, maintenance_update, maintenance_delete = crud_factory(
    model=EquipmentMaintenance,
    form_class=MaintenanceForm,
    list_template="inventory/maintenance/_table.html",
    form_template="inventory/maintenance/_form_modal.html",
    event_name="maintenance:refresh",
    qs_by_company=lambda company: EquipmentMaintenance.objects.filter(
        equipment__company=company
    ).select_related("equipment").order_by("equipment__name", "-last_date", "maintenance_type"),
    company_from_obj=lambda obj: obj.equipment.company,
    # Pasamos la compañía al form para filtrar equipos
    form_kwargs_fn=lambda company, instance=None: {"company": company},
)


# ---------------- Métodos de trabajo ----------------

method_list, method_create, method_update, method_delete = crud_factory(
    model=WorkMethod,
    form_class=WorkMethodForm,
    list_template="inventory/methods/_table.html",
    form_template="inventory/methods/_form_modal.html",
    event_name="methods:refresh",
    qs_by_company=lambda company: WorkMethod.objects.filter(company=company).order_by("modality"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Layout de planta ----------------

layout_list, layout_create, layout_update, layout_delete = crud_factory(
    model=PlantLayout,
    form_class=PlantLayoutForm,
    list_template="inventory/layout/_table.html",
    form_template="inventory/layout/_form_modal.html",
    event_name="layout:refresh",
    qs_by_company=lambda company: PlantLayout.objects.filter(company=company).order_by("layout_type"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Software ----------------

software_list, software_create, software_update, software_delete = crud_factory(
    model=SoftwareAsset,
    form_class=SoftwareAssetForm,
    list_template="inventory/software/_table.html",
    form_template="inventory/software/_form_modal.html",
    event_name="software:refresh",
    qs_by_company=lambda company: SoftwareAsset.objects.filter(company=company).order_by("usage", "name"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Materiales ----------------

material_list, material_create, material_update, material_delete = crud_factory(
    model=Material,
    form_class=MaterialForm,
    list_template="inventory/materials/_table.html",
    form_template="inventory/materials/_form_modal.html",
    event_name="materials:refresh",
    qs_by_company=lambda company: Material.objects.filter(company=company).order_by("category", "name"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Inversiones ----------------

investment_list, investment_create, investment_update, investment_delete = crud_factory(
    model=Investment,
    form_class=InvestmentForm,
    list_template="inventory/investments/_table.html",
    form_template="inventory/investments/_form_modal.html",
    event_name="investments:refresh",
    qs_by_company=lambda company: Investment.objects.filter(company=company).select_related("equipment").order_by(
        "-investment_date", "-investment_year", "-created_at"
    ),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
    form_kwargs_fn=lambda company, instance=None: {"company": company},
)


# ---------------- Talento (Workforce) ----------------

workforce_list, workforce_create, workforce_update, workforce_delete = crud_factory(
    model=WorkforceProfile,
    form_class=WorkforceProfileForm,
    list_template="inventory/workforce/_table.html",
    form_template="inventory/workforce/_form_modal.html",
    event_name="workforce:refresh",
    qs_by_company=lambda company: WorkforceProfile.objects.filter(company=company).order_by("area"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)


# ---------------- Disciplinas ----------------

discipline_list, discipline_create, discipline_update, discipline_delete = crud_factory(
    model=DisciplineAssessment,
    form_class=DisciplineAssessmentForm,
    list_template="inventory/disciplines/_table.html",
    form_template="inventory/disciplines/_form_modal.html",
    event_name="disciplines:refresh",
    qs_by_company=lambda company: DisciplineAssessment.objects.filter(company=company).order_by("item"),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)
