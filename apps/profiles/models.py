# apps/profiles/models.py
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models

from apps.inventory.models import TimeStampedModel  # tu base con created_at / updated_at

# leemos el nombre del modelo de compañía, pero NO lo resolvemos aún
COMPANY_MODEL = getattr(settings, "COMPANY_MODEL", "core.Company")


class Question(TimeStampedModel):
    """
    Catálogo de preguntas del instrumento
    """
    INSTRUMENT_CHOICES = [
        ("INNOVATION_PROFILE", "Innovation profile"),
        ("TECH_PROFILE", "Tech profile"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instrument_code = models.CharField(max_length=50, choices=INSTRUMENT_CHOICES)
    instrument_version = models.CharField(max_length=20)
    code = models.CharField(max_length=30)
    text = models.CharField(max_length=500)

    dimension = models.CharField(max_length=100, blank=True)
    sub_dimension = models.CharField(max_length=100, blank=True, null=True)

    level_1_label = models.CharField(max_length=400, blank=True)
    level_2_label = models.CharField(max_length=400, blank=True)
    level_3_label = models.CharField(max_length=400, blank=True)
    level_4_label = models.CharField(max_length=400, blank=True)

    weight = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("1"))
    is_active = models.BooleanField(default=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "profiles_question"
        ordering = ["instrument_code", "code"]
        unique_together = (("instrument_code", "instrument_version", "code"),)

    def __str__(self):
        return f"{self.instrument_code} {self.code}"


class Assessment(TimeStampedModel):
    """
    Aplicación del instrumento a una empresa en una fecha, por un analista.
    """
    INSTRUMENT_CHOICES = [
        ("INNOVATION_PROFILE", "Innovation profile"),
        ("TECH_PROFILE", "Tech profile"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 👇 usamos el string, NO get_model
    company = models.ForeignKey(
        COMPANY_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles_assessments",
    )

    instrument_code = models.CharField(max_length=50, choices=INSTRUMENT_CHOICES)
    instrument_version = models.CharField(max_length=20)
    assessment_date = models.DateField()
    analyst = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="profiles_assessments",
    )
    notes = models.TextField(blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "profiles_assessment"
        ordering = ["-assessment_date"]

    def __str__(self):
        return f"{self.instrument_code} - {self.assessment_date}"


class Response(TimeStampedModel):
    """
    Respuesta a una pregunta de un assessment concreto.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assessment = models.ForeignKey(
        "profiles.Assessment",  # string para evitar orden de carga
        on_delete=models.CASCADE,
        related_name="responses",
    )
    question = models.ForeignKey(
        "profiles.Question",
        on_delete=models.CASCADE,
        related_name="responses",
    )

    # 1..4
    answer_value = models.IntegerField()
    # decimal(6,2)
    score = models.DecimalField(max_digits=6, decimal_places=2)
    observations = models.TextField(blank=True)

    class Meta(TimeStampedModel.Meta):
        db_table = "profiles_response"
        unique_together = (("assessment", "question"),)
