from django import forms
from .models import Company

MUNICIPALITY_CHOICES = [
    ("Abejorral", "Abejorral"),
    ("Abriaquí", "Abriaquí"),
    ("Alejandría", "Alejandría"),
    ("Amagá", "Amagá"),
    ("Amalfi", "Amalfi"),
    ("Andes", "Andes"),
    ("Angelópolis", "Angelópolis"),
    ("Angostura", "Angostura"),
    ("Anorí", "Anorí"),
    ("Antioquia", "Antioquia"),
    ("Anzá", "Anzá"),
    ("Apartadó", "Apartadó"),
    ("Arboletes", "Arboletes"),
    ("Argelia", "Argelia"),
    ("Armenia", "Armenia"),
    ("Barbosa", "Barbosa"),
    ("Bello", "Bello"),
    ("Belmira", "Belmira"),
    ("Betania", "Betania"),
    ("Betulia", "Betulia"),
    ("Briceño", "Briceño"),
    ("Buriticá", "Buriticá"),
    ("Cáceres", "Cáceres"),
    ("Caicedo", "Caicedo"),
    ("Caldas", "Caldas"),
    ("Campamento", "Campamento"),
    ("Cañasgordas", "Cañasgordas"),
    ("Caracolí", "Caracolí"),
    ("Caramanta", "Caramanta"),
    ("Carepa", "Carepa"),
    ("Carolina del Príncipe", "Carolina del Príncipe"),
    ("Caucasia", "Caucasia"),
    ("Chigorodó", "Chigorodó"),
    ("Cisneros", "Cisneros"),
    ("Ciudad Bolívar", "Ciudad Bolívar"),
    ("Cocorná", "Cocorná"),
    ("Concepción", "Concepción"),
    ("Concordia", "Concordia"),
    ("Copacabana", "Copacabana"),
    ("Dabeiba", "Dabeiba"),
    ("Donmatías", "Donmatías"),
    ("Ebéjico", "Ebéjico"),
    ("El Bagre", "El Bagre"),
    ("Entrerríos", "Entrerríos"),
    ("Envigado", "Envigado"),
    ("Fredonia", "Fredonia"),
    ("Frontino", "Frontino"),
    ("Giraldo", "Giraldo"),
    ("Girardota", "Girardota"),
    ("Gómez Plata", "Gómez Plata"),
    ("Granada", "Granada"),
    ("Guadalupe", "Guadalupe"),
    ("Guarne", "Guarne"),
    ("Guatapé", "Guatapé"),
    ("Heliconia", "Heliconia"),
    ("Hispania", "Hispania"),
    ("Itagüí", "Itagüí"),
    ("Ituango", "Ituango"),
    ("Jardín", "Jardín"),
    ("Jericó", "Jericó"),
    ("La Ceja", "La Ceja"),
    ("La Estrella", "La Estrella"),
    ("La Pintada", "La Pintada"),
    ("La Unión", "La Unión"),
    ("Liborina", "Liborina"),
    ("Maceo", "Maceo"),
    ("Marinilla", "Marinilla"),
    ("Medellín", "Medellín"),
    ("Montebello", "Montebello"),
    ("Murindó", "Murindó"),
    ("Mutatá", "Mutatá"),
    ("Nariño", "Nariño"),
    ("Nechí", "Nechí"),
    ("Necoclí", "Necoclí"),
    ("Olaya", "Olaya"),
    ("Peñol", "Peñol"),
    ("Peque", "Peque"),
    ("Pueblorrico", "Pueblorrico"),
    ("Puerto Berrío", "Puerto Berrío"),
    ("Puerto Nare", "Puerto Nare"),
    ("Puerto Triunfo", "Puerto Triunfo"),
    ("Remedios", "Remedios"),
    ("Retiro", "Retiro"),
    ("Rionegro", "Rionegro"),
    ("Sabanalarga", "Sabanalarga"),
    ("Sabaneta", "Sabaneta"),
    ("Salgar", "Salgar"),
    ("San Andrés de Cuerquia", "San Andrés de Cuerquia"),
    ("San Carlos", "San Carlos"),
    ("San Francisco", "San Francisco"),
    ("San Jerónimo", "San Jerónimo"),
    ("San José de la Montaña", "San José de la Montaña"),
    ("San Juan de Urabá", "San Juan de Urabá"),
    ("San Luis", "San Luis"),
    ("San Pedro de los Milagros", "San Pedro de los Milagros"),
    ("San Pedro de Urabá", "San Pedro de Urabá"),
    ("San Rafael", "San Rafael"),
    ("San Roque", "San Roque"),
    ("San Vicente", "San Vicente"),
    ("Santa Bárbara", "Santa Bárbara"),
    ("Santa Fe de Antioquia", "Santa Fe de Antioquia"),
    ("Santa Rosa de Osos", "Santa Rosa de Osos"),
    ("Santo Domingo", "Santo Domingo"),
    ("Segovia", "Segovia"),
    ("Sonsón", "Sonsón"),
    ("Sopetrán", "Sopetrán"),
    ("Támesis", "Támesis"),
    ("Tarazá", "Tarazá"),
    ("Tarso", "Tarso"),
    ("Titiribí", "Titiribí"),
    ("Toledo", "Toledo"),
    ("Turbo", "Turbo"),
    ("Uramita", "Uramita"),
    ("Urrao", "Urrao"),
    ("Valdivia", "Valdivia"),
    ("Valparaíso", "Valparaíso"),
    ("Vegachí", "Vegachí"),
    ("Venecia", "Venecia"),
    ("Vigía del Fuerte", "Vigía del Fuerte"),
    ("Yalí", "Yalí"),
    ("Yarumal", "Yarumal"),
    ("Yolombó", "Yolombó"),
    ("Yondó", "Yondó"),
    ("Zaragoza", "Zaragoza"),
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
