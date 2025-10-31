# apps/inventory/forms.py
from django import forms
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
from datetime import date
from django.utils import timezone

BASE_INPUT = (
    "block w-full rounded-lg border border-gray-300 bg-white "
    "px-3 py-2 text-sm text-gray-900 shadow-sm "
    "focus:border-emerald-600 focus:ring-2 focus:ring-emerald-600 "
    "placeholder:text-gray-400"
)

BASE_TEXTAREA = BASE_INPUT + " resize-y"
BASE_SELECT = (
    "block w-full rounded-lg border border-gray-300 bg-white "
    "px-3 py-2 text-sm text-gray-900 shadow-sm "
    "focus:border-emerald-600 focus:ring-2 focus:ring-emerald-600"
)

BASE_DATE = (
    "block w-full rounded-lg border border-gray-300 bg-white "
    "px-3 py-2 text-sm text-gray-900 shadow-sm "
    "focus:border-emerald-600 focus:ring-2 focus:ring-emerald-600"
)
BASE_SELECT_MULTI = BASE_SELECT + " h-36"


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            "name",
            "category",
            "quantity",
            "purchase_year",
            "purchase_origin",
            "utilization_pct",  # 0–100
            "energy_sources",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": BASE_INPUT,
                    "placeholder": "p. ej. Horno rotatorio",
                    "autofocus": True,
                }
            ),
            "category": forms.Select(attrs={"class": BASE_SELECT}),
            "quantity": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 1, "step": 1, "placeholder": "1"}
            ),
            "purchase_year": forms.NumberInput(
                attrs={
                    "class": BASE_INPUT,
                    "min": 1950,
                    "max": 3000,
                    "step": 1,
                    "placeholder": str(date.today().year),
                }
            ),
            "purchase_origin": forms.Select(attrs={"class": BASE_SELECT}),
            "utilization_pct": forms.NumberInput(
                attrs={
                    "class": BASE_INPUT,
                    "min": 0,
                    "max": 100,
                    "step": "0.01",
                    "placeholder": "0-100",
                }
            ),
            "energy_sources": forms.SelectMultiple(attrs={"class": BASE_SELECT_MULTI}),
            "description": forms.Textarea(
                attrs={
                    "class": BASE_TEXTAREA,
                    "rows": 3,
                    "placeholder": "Notas adicionales del equipo…",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # defaults suaves
        self.fields["quantity"].initial = self.fields["quantity"].initial or 1
        self.fields["purchase_year"].initial = (
            self.fields["purchase_year"].initial or date.today().year
        )


class TechnicalServiceForm(forms.ModelForm):
    class Meta:
        model = TechnicalService
        fields = [
            "service_type",
            "provider_name",
            "service_description",
            "service_location",
            "notes",
        ]
        labels = {
            "service_type": "Tipo de servicio",
            "provider_name": "Proveedor",
            "service_description": "Servicio (descripción)",
            "service_location": "Lugar de la prestación",
            "notes": "Observaciones",
        }
        help_texts = {
            "service_location": "Selecciona si el servicio se realiza en sitio o fuera de sitio.",
        }
        widgets = {
            # Los CharField con choices ya salen como <select> automáticamente;
            # aquí solo damos estilo y placeholder.
            "service_type": forms.Select(
                attrs={"class": BASE_SELECT, "data-placeholder": "Selecciona un tipo"}
            ),
            "service_location": forms.Select(
                attrs={"class": BASE_SELECT, "data-placeholder": "Selecciona el lugar"}
            ),
            "provider_name": forms.TextInput(
                attrs={
                    "class": BASE_INPUT,
                    "placeholder": "Nombre del proveedor",
                    "autocomplete": "off",
                }
            ),
            "service_description": forms.TextInput(
                attrs={
                    "class": BASE_INPUT,
                    "placeholder": "p. ej. Mantenimiento correctivo de horno",
                    "autocomplete": "off",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": BASE_TEXTAREA,
                    "rows": 3,
                    "placeholder": "Notas u observaciones",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar requeridos según el diccionario de datos
        self.fields["service_type"].required = True
        self.fields["provider_name"].required = True
        # Los otros pueden quedar opcionales (ya están con blank=True/null=True)
        # Añadimos opción vacía visible cuando el campo es opcional:
        if self.fields["service_location"].required is False:
            self.fields["service_location"].choices = [("", "---------")] + list(
                self.fields["service_location"].choices
            )


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = EquipmentMaintenance
        fields = ["equipment", "maintenance_type", "frequency", "last_date", "notes"]

        labels = {
            "equipment": "Equipo",
            "maintenance_type": "Tipo de mantenimiento",
            "frequency": "Frecuencia planificada",
            "last_date": "Última fecha realizada",
            "notes": "Observaciones",
        }

        help_texts = {
            "frequency": "Opcional.",
            "last_date": "Opcional. Formato AAAA-MM-DD.",
        }

        widgets = {
            "equipment": forms.Select(
                attrs={
                    "class": BASE_SELECT,
                    "placeholder": "Selecciona el equipo",
                }
            ),
            "maintenance_type": forms.Select(
                attrs={
                    "class": BASE_SELECT,
                }
            ),
            "frequency": forms.Select(
                attrs={
                    "class": BASE_SELECT,
                }
            ),
            "last_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": BASE_DATE,
                    "autocomplete": "off",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": BASE_TEXTAREA,
                    "placeholder": "Notas u observaciones…",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Acepta `company=<Company>` para filtrar los equipos al crear/editar.
        """
        company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)

        # Filtra equipos por empresa si se pasó `company`
        if company is not None:
            self.fields["equipment"].queryset = Equipment.objects.filter(  # type: ignore
                company=company
            ).order_by(
                "name"
            )

        # Etiquetas vacías amigables
        self.fields["equipment"].empty_label = "---------"  # type: ignore
        self.fields["frequency"].required = False  # ya está blank=True, explicitamos

    def clean_last_date(self):
        """
        Si decides que 'última fecha' no puede ser futura, valida aquí.
        Comenta el bloque si quieres permitir fechas futuras.
        """
        last_date = self.cleaned_data.get("last_date")
        if last_date and last_date > timezone.localdate():
            raise forms.ValidationError("La última fecha no puede ser futura.")
        return last_date


# ---------------- Additional model forms ----------------


class WorkMethodForm(forms.ModelForm):
    class Meta:
        model = WorkMethod
        fields = ["modality", "description", "shift_pattern", "shifts_count"]
        widgets = {
            "modality": forms.Select(attrs={"class": BASE_SELECT}),
            "description": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Notas u observaciones"}
            ),
            "shift_pattern": forms.TextInput(
                attrs={"class": BASE_INPUT, "placeholder": "p. ej. 2x8, 3x8"}
            ),
            "shifts_count": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "step": 1}
            ),
        }


class PlantLayoutForm(forms.ModelForm):
    class Meta:
        model = PlantLayout
        fields = ["layout_type", "description"]
        widgets = {
            "layout_type": forms.Select(attrs={"class": BASE_SELECT}),
            "description": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Descripción o notas"}
            ),
        }


class SoftwareAssetForm(forms.ModelForm):
    class Meta:
        model = SoftwareAsset
        fields = ["usage", "name", "description", "area"]
        widgets = {
            "usage": forms.Select(attrs={"class": BASE_SELECT}),
            "name": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Nombre del software"}),
            "description": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Notas o alcance"}
            ),
            "area": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Área/Proceso"}),
        }


class DisciplineAssessmentForm(forms.ModelForm):
    class Meta:
        model = DisciplineAssessment
        fields = ["item", "importance_score", "adoption_level", "notes"]
        widgets = {
            "item": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Disciplina / saber"}),
            "importance_score": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 1, "max": 5, "step": 1}
            ),
            "adoption_level": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "max": 4, "step": 1}
            ),
            "notes": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Comentarios"}
            ),
        }


class WorkforceProfileForm(forms.ModelForm):
    class Meta:
        model = WorkforceProfile
        fields = [
            "area",
            "people_count",
            "education_level",
            "avg_experience_years",
            "notes",
        ]
        widgets = {
            "area": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Área"}),
            "people_count": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "step": 1}
            ),
            "education_level": forms.Select(attrs={"class": BASE_SELECT}),
            "avg_experience_years": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "step": 0.1}
            ),
            "notes": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Notas"}
            ),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "category",
            "name",
            "origin",
            "inventory_management",
            "cost_share_pct",
            "notes",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": BASE_SELECT}),
            "name": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Nombre del material"}),
            "origin": forms.Select(attrs={"class": BASE_SELECT}),
            "inventory_management": forms.Select(attrs={"class": BASE_SELECT}),
            "cost_share_pct": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "max": 100, "step": 0.01}
            ),
            "notes": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Notas"}
            ),
        }


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = [
            "category",
            "item_name",
            "motive",
            "amount_cop",
            "funding_source",
            "funding_entity",
            "investment_date",
            "investment_year",
            "status",
            "equipment",
            "equipment_category",
            "notes",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": BASE_SELECT}),
            "item_name": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Ítem / proyecto"}),
            "motive": forms.Select(attrs={"class": BASE_SELECT}),
            "amount_cop": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 0, "step": 0.01}
            ),
            "funding_source": forms.Select(attrs={"class": BASE_SELECT}),
            "funding_entity": forms.TextInput(attrs={"class": BASE_INPUT, "placeholder": "Entidad (opcional)"}),
            "investment_date": forms.DateInput(
                attrs={"type": "date", "class": BASE_DATE}
            ),
            "investment_year": forms.NumberInput(
                attrs={"class": BASE_INPUT, "min": 1950, "max": 3000, "step": 1}
            ),
            "status": forms.Select(attrs={"class": BASE_SELECT}),
            "equipment": forms.Select(attrs={"class": BASE_SELECT}),
            "equipment_category": forms.Select(attrs={"class": BASE_SELECT}),
            "notes": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "rows": 3, "placeholder": "Notas"}
            ),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company", None)
        super().__init__(*args, **kwargs)
        if company is not None:
            self.fields["equipment"].queryset = Equipment.objects.filter(company=company).order_by("name")  # type: ignore
        # Provide friendly empty option for optional selects
        for name in ("status", "equipment", "equipment_category"):
            if name in self.fields and not self.fields[name].required:
                choices = list(self.fields[name].choices)
                self.fields[name].choices = [("", "---------")] + choices
