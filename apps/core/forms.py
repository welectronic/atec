from django import forms
from .models import Company

MUNICIPALITY_CHOICES = [
    ("Bogotá", "Bogotá"),
    ("Medellín", "Medellín"),
    ("Cali", "Cali"),
    ("Barranquilla", "Barranquilla"),
]

class CompanyForm(forms.ModelForm):
    municipality = forms.ChoiceField(choices=MUNICIPALITY_CHOICES, required=True, label="Municipio")
    contact_phone = forms.CharField(required=True, label="Celular de contacto")
    contact_email = forms.EmailField(required=True, label="Email de contacto")
    assessment_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="Fecha")

    class Meta:
        model = Company
        fields = [
            "name", "tax_id", "municipality", "org_type",
            "contact_name", "contact_email", "contact_phone",
            "advisor", "assessment_date", "organization", "description",
        ]
        widgets = {
            "assessment_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = "block w-full rounded-md border-gray-300 shadow-sm focus:border-brand focus:ring-brand"
        for name, field in self.fields.items():
            css = base
            if isinstance(field.widget, forms.Textarea):
                css += " min-h-28"
            field.widget.attrs.setdefault("class", css)

    def clean_tax_id(self):
        tax_id = self.cleaned_data["tax_id"].strip()
        # Agrega reglas específicas si lo deseas
        return tax_id
