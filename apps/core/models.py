# apps/core/models.py
from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    class CompanyType(models.TextChoices):
        ORGANIZATION = "organization", "Organización"
        ENTREPRENEURSHIP = "entrepreneurship", "Emprendimiento"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="companies"
    )

    # Instrumento
    assessment_date = models.DateField(null=True, blank=True, verbose_name="Fecha")
    name = models.CharField(max_length=255, verbose_name="Nombre de la empresa")
    tax_id = models.CharField(max_length=64, unique=True, verbose_name="NIT")
    municipality = models.CharField(max_length=128, verbose_name="Municipio")

    contact_name = models.CharField(max_length=255, verbose_name="Nombre de contacto")
    contact_role = models.CharField(max_length=128, verbose_name="Cargo del contacto")
    contact_email = models.EmailField(verbose_name="Email de contacto")
    contact_phone = models.CharField(max_length=32, verbose_name="Celular de contacto")

    org_type = models.CharField(
        max_length=32, choices=CompanyType.choices, default=CompanyType.ORGANIZATION,
        verbose_name="Tipo de organización",
    )
    description = models.TextField(blank=True, verbose_name="Descripción de la organización")

    advisor = models.ForeignKey(  # Asesor empresarial principal
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="advised_companies",
        verbose_name="Asesor empresarial",
    )

    status = models.CharField(max_length=32, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.name} ({self.tax_id})"


class AnalystCompany(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_companies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="analysts")
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "company")
