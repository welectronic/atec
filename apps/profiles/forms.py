# apps/profiles/forms.py
from django import forms
from django.conf import settings

from .models import Question, Assessment, Response


class TailwindModelForm(forms.ModelForm):
    """
    Basecita para aplicar clases comunes.
    Si ya tienes una base en otro lado, puedes cambiar esta.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.EmailInput, forms.URLInput)):
                field.widget.attrs["class"] = "w-full rounded-lg border-gray-300 focus:border-green-500 focus:ring-green-500 text-sm"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] = "w-full rounded-lg border-gray-300 focus:border-green-500 focus:ring-green-500 text-sm"
                field.widget.attrs["rows"] = 3
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs["class"] = "w-full rounded-lg border-gray-300 focus:border-green-500 focus:ring-green-500 text-sm"


class AssessmentForm(TailwindModelForm):
    assessment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha de evaluación",
    )

    class Meta:
        model = Assessment
        # company y analyst los vamos a setear en la vista
        fields = [
            "instrument_code",
            "instrument_version",
            "assessment_date",
            "notes",
        ]
        labels = {
            "instrument_code": "Instrumento",
            "instrument_version": "Versión",
            "notes": "Observaciones",
        }


class QuestionForm(TailwindModelForm):
    class Meta:
        model = Question
        fields = [
            "instrument_code",
            "instrument_version",
            "code",
            "text",
            "dimension",
            "sub_dimension",
            "level_1_label",
            "level_2_label",
            "level_3_label",
            "level_4_label",
            "weight",
            "is_active",
        ]
        labels = {
            "instrument_code": "Instrumento",
            "instrument_version": "Versión",
            "code": "Código",
            "text": "Pregunta",
            "dimension": "Dimensión",
            "sub_dimension": "Subdimensión",
            "level_1_label": "Nivel 1 (descriptivo)",
            "level_2_label": "Nivel 2 (descriptivo)",
            "level_3_label": "Nivel 3 (descriptivo)",
            "level_4_label": "Nivel 4 (descriptivo)",
            "weight": "Peso",
            "is_active": "Activo",
        }


class ResponseForm(TailwindModelForm):
    class Meta:
        model = Response
        # assessment y question los setea la vista
        fields = [
            "answer_value",
            "score",
            "observations",
        ]
        labels = {
            "answer_value": "Respuesta (1-4)",
            "score": "Puntaje",
            "observations": "Observaciones",
        }
        widgets = {
            "answer_value": forms.NumberInput(attrs={"min": 1, "max": 4}),
        }
