# inventory/models.py
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator  # type: ignore
from django.utils import timezone

# === Ajusta esto si tu modelo Company está en otro app ===
COMPANY_MODEL = getattr(settings, "COMPANY_MODEL", "core.Company")  # e.g., "companies.Company"

# Utilidad para validadores de año
def current_year():
    return timezone.now().year

# Base con timestamps
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -------------------------
# Catálogos y Choices
# -------------------------
class EquipmentCategory(models.TextChoices):
    CORE = "CORE", "Core / Medular"
    AUXILIARY = "AUXILIARY", "Auxiliary / Periférico"

class EnergyTypeCode(models.TextChoices):
    ELECTRICITY = "ELECTRICITY", "Electricity"
    DIESEL = "DIESEL", "Diesel"
    GASOLINE = "GASOLINE", "Gasoline"
    NATURAL_GAS = "NATURAL_GAS", "Natural Gas"
    LPG = "LPG", "LPG"
    SOLAR = "SOLAR", "Solar"
    STEAM = "STEAM", "Steam"
    MANUAL = "MANUAL", "Manual"
    OTHER = "OTHER", "Other"

class ServiceType(models.TextChoices):
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    CALIBRATION = "CALIBRATION", "Calibration"
    REPAIR = "REPAIR", "Repair"
    SOFTWARE_SUPPORT = "SOFTWARE_SUPPORT", "Software support"
    TRAINING = "TRAINING", "Training"
    OTHER = "OTHER", "Other"

class ServiceLocation(models.TextChoices):
    ON_SITE = "ON_SITE", "On-site"
    OFF_SITE = "OFF_SITE", "Off-site"
    OTHER = "OTHER", "Other"

class MaintenanceType(models.TextChoices):
    PREVENTIVE = "PREVENTIVE", "Preventive"
    CORRECTIVE = "CORRECTIVE", "Corrective"
    PREDICTIVE = "PREDICTIVE", "Predictive"
    CALIBRATION = "CALIBRATION", "Calibration"
    OTHER = "OTHER", "Other"

class MaintenanceFrequency(models.TextChoices):
    DAILY = "DAILY", "Daily"
    WEEKLY = "WEEKLY", "Weekly"
    MONTHLY = "MONTHLY", "Monthly"
    QUARTERLY = "QUARTERLY", "Quarterly"
    SEMIANNUAL = "SEMIANNUAL", "Semiannual"
    ANNUAL = "ANNUAL", "Annual"
    USAGE_BASED = "USAGE_BASED", "Usage-based"

class WorkModality(models.TextChoices):
    CONTINUOUS = "CONTINUOUS", "Continuous"
    BATCH = "BATCH", "Batch"
    MAKE_TO_ORDER = "MAKE_TO_ORDER", "Make-to-order"
    OUTSOURCING_MAQUILA = "OUTSOURCING_MAQUILA", "Outsourcing / Maquila"
    SERVUCTION_FRONT_BACK = "SERVUCTION_FRONT_BACK", "Servuction front/back"
    OTHER = "OTHER", "Other"

class LayoutType(models.TextChoices):
    FUNCTIONAL = "FUNCTIONAL", "Functional / Process"
    PRODUCT_LINE = "PRODUCT_LINE", "Product / Line"
    CELLULAR = "CELLULAR", "Cellular"
    FIXED_POSITION = "FIXED_POSITION", "Fixed-position"
    HYBRID = "HYBRID", "Hybrid"
    WAREHOUSE = "WAREHOUSE", "Warehouse"

class SoftwareUsage(models.TextChoices):
    ERP = "ERP", "ERP"
    CRM = "CRM", "CRM"
    ACCOUNTING = "ACCOUNTING", "Accounting"
    INVENTORY = "INVENTORY", "Inventory"
    PRODUCTION = "PRODUCTION", "Production"
    QUALITY = "QUALITY", "Quality"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    PAYROLL = "PAYROLL", "Payroll"
    BI = "BI", "Business Intelligence / Analytics"
    OFFICE = "OFFICE", "Office / Productivity"
    OTHER = "OTHER", "Other"

class MaterialCategory(models.TextChoices):
    RAW_MATERIAL = "RAW_MATERIAL", "Raw material"
    SUPPLY = "SUPPLY", "Supply / Input"

class MaterialOrigin(models.TextChoices):
    NATIONAL = "NATIONAL", "National"
    IMPORTED = "IMPORTED", "Imported"
    LOCAL = "LOCAL", "Local"
    OWN_PRODUCTION = "OWN_PRODUCTION", "Own production"
    OTHER = "OTHER", "Other"

class InventoryPolicy(models.TextChoices):
    NO_FORMAL = "NO_FORMAL", "No formal"
    MIN_MAX = "MIN_MAX", "Min-Max"
    ABC = "ABC", "ABC"
    JIT = "JIT", "JIT"
    KANBAN = "KANBAN", "Kanban"
    FIFO = "FIFO", "FIFO"
    LIFO = "LIFO", "LIFO"
    FEFO = "FEFO", "FEFO"
    CONSIGNMENT = "CONSIGNMENT", "Consignment"
    OTHER = "OTHER", "Other"

class InvestmentCategory(models.TextChoices):
    EQUIPMENT = "EQUIPMENT", "Equipment / Machinery"
    TECH_DEVELOPMENT = "TECH_DEVELOPMENT", "Technological development"

class InvestmentMotive(models.TextChoices):
    REPLACEMENT = "REPLACEMENT", "Replacement"
    CAPACITY_EXPANSION = "CAPACITY_EXPANSION", "Capacity expansion"
    MODERNIZATION_AUTOMATION = "MODERNIZATION_AUTOMATION", "Modernization / Automation"
    QUALITY_COMPLIANCE = "QUALITY_COMPLIANCE", "Quality / Compliance"
    NEW_PRODUCT = "NEW_PRODUCT", "New product"
    ENERGY_EFFICIENCY = "ENERGY_EFFICIENCY", "Energy efficiency"
    DIGITALIZATION = "DIGITALIZATION", "Digitalization"
    R_AND_D = "R_AND_D", "R&D / Tech development"
    CERTIFICATION = "CERTIFICATION", "Certification"
    OTHER = "OTHER", "Other"

class FundingSource(models.TextChoices):
    OWN_FUNDS = "OWN_FUNDS", "Own funds"
    BANK_CREDIT = "BANK_CREDIT", "Bank credit"
    SUPPLIER_CREDIT = "SUPPLIER_CREDIT", "Supplier credit"
    LEASING = "LEASING", "Leasing"
    PUBLIC_GRANT = "PUBLIC_GRANT", "Public grant"
    COFINANCING = "COFINANCING", "Cofinancing"
    VENTURE = "VENTURE", "Venture / Equity"
    OTHER = "OTHER", "Other"

class InvestmentStatus(models.TextChoices):
    PLANNED = "PLANNED", "Planned"
    APPROVED = "APPROVED", "Approved"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    EXECUTED = "EXECUTED", "Executed"


# -------------------------
# Entidades
# -------------------------
class EnergySource(TimeStampedModel):
    code = models.CharField(
        max_length=30,
        choices=EnergyTypeCode.choices,
        unique=True,
        db_index=True,
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Energy source"
        verbose_name_plural = "Energy sources"
        ordering = ("code",)

    def __str__(self):
        return f"{getattr(self, 'get_code_display')()}"


class Equipment(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="equipments")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=EquipmentCategory.choices, db_index=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    purchase_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1950), MaxValueValidator(3000)]
    )
    purchase_origin = models.CharField(max_length=50, blank=True, null=True)  # libre o catalógalo si quieres
    utilization_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    description = models.TextField(blank=True, null=True)

    # M2M explícito vía tabla puente
    energy_sources = models.ManyToManyField(
        EnergySource, through="EquipmentEnergy", related_name="equipments", blank=True
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["company", "name"]),
        ]
        ordering = ("name", "id")
    
    class PurchaseOrigin(models.TextChoices):
        NATIONAL  = "NATIONAL",  "Nacional"
        IMPORTED  = "IMPORTED",  "Importado"
        DONATION  = "DONATION",  "Donación"
        LEASE     = "LEASE",     "Leasing / Arrendamiento"
        IN_HOUSE  = "IN_HOUSE",  "Fabricación propia"
        OTHER     = "OTHER",     "Otro"

    purchase_origin = models.CharField(
        "Origen de compra",
        max_length=20,
        choices=PurchaseOrigin.choices,
        blank=True,    # muestra opción vacía "--------"
        null=True,
        help_text="Selecciona el origen de adquisición del equipo.",
    )

    def __str__(self):
        return f"{self.name} ({getattr(self, 'get_category_display')()})"


class EquipmentEnergy(TimeStampedModel):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="equipment_energies")
    energy_source = models.ForeignKey(EnergySource, on_delete=models.CASCADE, related_name="energy_equipments")
    notes = models.CharField(max_length=200, blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Equipment-Energy relation"
        verbose_name_plural = "Equipment-Energy relations"
        constraints = [
            models.UniqueConstraint(fields=["equipment", "energy_source"], name="uq_equipment_energy_source")
        ]

    def __str__(self):
        return f"{self.equipment} - {self.energy_source}"


class TechnicalService(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="technical_services")
    service_type = models.CharField(max_length=50, choices=ServiceType.choices)
    provider_name = models.CharField(max_length=200)
    service_description = models.CharField(max_length=300, blank=True, null=True)
    service_location = models.CharField(max_length=100, choices=ServiceLocation.choices, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Technical service"
        verbose_name_plural = "Technical services"
        indexes = [models.Index(fields=["company", "service_type"])]

    def __str__(self):
        return f"{self.provider_name} - {getattr(self, 'get_service_type_display')()}"


class EquipmentMaintenance(TimeStampedModel):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="maintenances")
    maintenance_type = models.CharField(max_length=50, choices=MaintenanceType.choices)
    frequency = models.CharField(max_length=50, choices=MaintenanceFrequency.choices, blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Equipment maintenance"
        verbose_name_plural = "Equipment maintenances"
        indexes = [models.Index(fields=["equipment", "maintenance_type"])]

    def __str__(self):
        return f"{self.equipment} - {getattr(self, 'get_maintenance_type_display')()}"


class WorkMethod(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="work_methods")
    modality = models.CharField(max_length=150, choices=WorkModality.choices)
    description = models.TextField(blank=True, null=True)
    shift_pattern = models.CharField(max_length=120, blank=True, null=True)
    shifts_count = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Work method"
        verbose_name_plural = "Work methods"
        indexes = [models.Index(fields=["company", "modality"])]

    def __str__(self):
        return f"{getattr(self, 'get_modality_display')()}"


class PlantLayout(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="plant_layouts")
    layout_type = models.CharField(max_length=80, choices=LayoutType.choices)
    description = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Plant layout"
        verbose_name_plural = "Plant layouts"
        indexes = [models.Index(fields=["company", "layout_type"])]

    def __str__(self):
        return f"{getattr(self, 'get_layout_type_display')()}"


class SoftwareAsset(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="software_assets")
    usage = models.CharField(max_length=120, choices=SoftwareUsage.choices)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Software asset"
        verbose_name_plural = "Software assets"
        unique_together = (("company", "name"),)
        indexes = [models.Index(fields=["company", "usage"])]

    def __str__(self):
        return f"{self.name} ({getattr(self, 'get_usage_display')()})"


class DisciplineAssessment(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="discipline_assessments")
    item = models.CharField(max_length=150)
    importance_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    adoption_level = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Discipline assessment"
        verbose_name_plural = "Discipline assessments"
        indexes = [models.Index(fields=["company", "item"])]

    def __str__(self):
        return f"{self.item} (Imp:{self.importance_score} / Adopt:{self.adoption_level})"


class WorkforceProfile(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="workforce_profiles")
    area = models.CharField(max_length=100)
    people_count = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    education_level = models.CharField(
        max_length=40,
        choices=(
            ("BASICA", "Básica"),
            ("MEDIA", "Media"),
            ("TECNICO", "Técnico"),
            ("TECNOLOGO", "Tecnólogo"),
            ("PROFESIONAL", "Profesional"),
            ("ESPECIALIZACION", "Especialización"),
            ("MAESTRIA", "Maestría"),
            ("DOCTORADO", "Doctorado"),
        ),
    )
    avg_experience_years = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,
                                               validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Workforce profile"
        verbose_name_plural = "Workforce profiles"
        unique_together = (("company", "area"),)
        indexes = [models.Index(fields=["company", "area"])]

    def __str__(self):
        return f"{self.area} - {self.people_count} ppl"


class Material(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="materials")
    category = models.CharField(max_length=20, choices=MaterialCategory.choices)
    name = models.CharField(max_length=150)
    origin = models.CharField(max_length=50, choices=MaterialOrigin.choices, blank=True, null=True)
    inventory_management = models.CharField(max_length=50, choices=InventoryPolicy.choices, blank=True, null=True)
    cost_share_pct = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Share of total material cost (0-100)"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        unique_together = (("company", "name"),)
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["company", "name"]),
        ]

    def __str__(self):
        return f"{self.name} ({getattr(self, 'get_category_display')()})"


class Investment(TimeStampedModel):
    company = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, related_name="investments")
    category = models.CharField(max_length=30, choices=InvestmentCategory.choices)
    item_name = models.CharField(max_length=200)
    motive = models.CharField(max_length=40, choices=InvestmentMotive.choices)
    amount_cop = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    funding_source = models.CharField(max_length=80, choices=FundingSource.choices)
    funding_entity = models.CharField(max_length=150, blank=True, null=True)
    # Dos alternativas para fecha
    investment_date = models.DateField(blank=True, null=True)
    investment_year = models.PositiveSmallIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1950), MaxValueValidator(3000)],
        help_text="If exact date is unknown"
    )
    status = models.CharField(max_length=20, choices=InvestmentStatus.choices, blank=True, null=True)

    # Enlace opcional con un equipo concreto
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, blank=True, null=True, related_name="investments")
    equipment_category = models.CharField(
        max_length=20, choices=EquipmentCategory.choices, blank=True, null=True,
        help_text="If the investment explicitly targets CORE/AUXILIARY machinery"
    )

    notes = models.TextField(blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "Investment"
        verbose_name_plural = "Investments"
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["company", "motive"]),
        ]
        ordering = ("-investment_date", "-investment_year", "-created_at")

    def __str__(self):
        return f"{self.item_name} - {getattr(self, 'get_category_display')()} ({self.amount_cop} COP)"

