# AlimentaTec Antioquia - Portal de Inventario Tecnológico

Sistema web para la gestión y evaluación del inventario tecnológico de empresas participantes en el programa AlimentaTec Antioquia, desarrollado para el CIB (Centro de Innovación y Bienestar) y la Gobernación de Antioquia.

## 📋 Descripción General

Portal Django que permite a asesores empresariales y analistas registrar, gestionar y evaluar el inventario tecnológico de empresas del sector alimentario en Antioquia. El sistema implementa un modelo de permisos basado en roles con Row-Level Security (RLS) para garantizar que cada usuario solo acceda a las empresas asignadas.

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

**Backend:**

- **Django 5.2.7** - Framework web principal
- **Python 3.x** - Lenguaje de programación
- **PostgreSQL** - Base de datos relacional con soporte SSL
- **python-dotenv** - Gestión de variables de entorno
- **django-filters** - Filtrado avanzado de querysets

**Frontend:**

- **Tailwind CSS 3.x** (CDN) - Framework CSS utility-first
- **HTMX 1.9.12** - Interactividad sin JavaScript complejo
- **Lucide Icons** - Biblioteca de iconos SVG
- **Django Templates** - Motor de plantillas server-side

**Infraestructura:**

- **DigitalOcean** - Hosting y base de datos gestionada
- **Caddy** - Servidor web con HTTPS automático
- **systemd** - Gestión de servicios en producción

### Patrón de Arquitectura

El proyecto sigue una arquitectura **modular basada en Django Apps** con separación de responsabilidades:

``` batch
portal/                 # Configuración del proyecto Django
├── settings.py        # Configuración centralizada
├── urls.py            # Enrutamiento principal
├── wsgi.py            # WSGI application
└── asgi.py            # ASGI application (preparado para async)

apps/                   # Aplicaciones Django modulares
├── accounts/          # Autenticación y usuarios (UUID-based)
├── core/              # Modelos de negocio centrales (Company, Organization)
├── inventory/         # Gestión de inventario tecnológico (11 módulos)
├── profiles/          # Perfiles de innovación y tecnología ⭐ NUEVO
├── api/               # API REST (estructura preparada)
├── auditing/          # Auditoría de cambios
├── common/            # Utilidades compartidas (context processors)
├── diagnostics/       # Diagnósticos empresariales
├── documents/         # Gestión documental
└── reports/           # Generación de reportes

db/                     # Scripts de base de datos
├── ddl/               # Data Definition Language
│   └── rls/          # Row-Level Security policies
├── seeds/             # Datos iniciales
└── maintenance/       # Scripts de mantenimiento

infra/                  # Infraestructura como código
├── do/                # DigitalOcean configs
│   ├── caddy/        # Configuración Caddy
│   └── systemd/      # Servicios systemd
├── docker/            # Dockerfiles (preparado)
└── github-actions/    # CI/CD workflows

templates/              # Plantillas Django
├── base.html          # Layout base
├── core/              # Templates de empresas
├── inventory/         # Templates de inventario
│   └── tabs/         # Componentes por pestaña
├── components/        # Componentes reutilizables
└── includes/          # Partials

static_src/             # Assets fuente
└── src/
    ├── css/           # Estilos personalizados
    └── js/            # JavaScript personalizado
```

## 🔐 Sistema de Permisos y Seguridad

### Modelo de Autenticación

**Custom User Model:**

```python
# apps/accounts/models.py
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(max_length=255)
```

### Row-Level Security (RLS)

El sistema implementa RLS a nivel de aplicación mediante:

1. **Selector Pattern** (`apps/core/selectors.py`):

```python
def get_allowed_company_ids(user) -> Set[int]:
    """
    Retorna IDs de empresas accesibles según:
    - Superuser: acceso total
    - Advisor: empresas donde es advisor
    - Analyst: empresas asignadas vía AnalystCompany
    """
```

2. **CompanyScopeMixin** para Class-Based Views:

```python
class CompanyScopeMixin(View):
    """Filtra automáticamente querysets por empresas permitidas"""
    def get_queryset(self):
        return self.filter_queryset_by_scope(qs)
```

3. **Decorator para Function-Based Views**:

```python
@require_company_access(lambda request, pk: pk)
def company_detail(request, pk):
    # Solo accesible si user tiene permiso sobre company_id=pk
```

### Relaciones de Acceso

``` batch
User (Superuser) → Acceso total
User (Advisor) → Company.advisor FK → Empresas asesoradas
User (Analyst) → AnalystCompany M2M → Empresas asignadas
```

## 📊 Modelo de Datos

### Entidades Principales

**Core (apps/core/models.py):**

- `Organization` - Organización matriz
- `Company` - Empresa participante (NIT, contacto, tipo, municipio)
- `AnalystCompany` - Relación M2M User-Company para analistas

**Profiles (apps/profiles/models.py):** ⭐ NUEVO

- `Question` - Catálogo de preguntas de instrumentos (UUID, dimensiones, niveles 1-4)
- `Assessment` - Evaluaciones aplicadas a empresas (UUID, fecha, analista)
- `Response` - Respuestas a preguntas (answer_value 1-4, score decimal)

**Inventory (apps/inventory/models.py):**

**Equipamiento:**

- `Equipment` - Equipos y maquinaria (CORE/AUXILIARY)
- `EnergySource` - Fuentes energéticas (catálogo)
- `EquipmentEnergy` - Relación M2M Equipment-EnergySource
- `EquipmentMaintenance` - Planes de mantenimiento

**Servicios y Métodos:**

- `TechnicalService` - Servicios técnicos externos
- `WorkMethod` - Modalidades de trabajo (continuo, batch, maquila)
- `PlantLayout` - Distribución de planta (funcional, celular, línea)

**Software y Talento:**

- `SoftwareAsset` - Activos de software (ERP, CRM, etc.)
- `WorkforceProfile` - Perfiles de talento por área
- `DisciplineAssessment` - Evaluación de saberes/disciplinas

**Materiales e Inversiones:**

- `Material` - Materias primas e insumos
- `Investment` - Inversiones tecnológicas (categoría, monto, fuente)

### Características del Modelo

- **TimeStampedModel** base abstracto con `created_at` / `updated_at`
- **Choices enumerados** con `TextChoices` para catálogos
- **Validadores Django** (MinValueValidator, MaxValueValidator)
- **Índices compuestos** para optimización de queries
- **Constraints únicos** para integridad referencial

## 🎨 Frontend y UX

### Arquitectura Frontend

**Patrón HTMX + Django Templates:**

- **Sin SPA**: Renderizado server-side con interactividad HTMX
- **Modales dinámicos**: Carga de formularios vía AJAX
- **Actualización parcial**: Swap de contenido sin recargar página
- **Eventos personalizados**: `HX-Trigger` para sincronización
- **Template tags custom**: Filtros para profiles (get_response)

### Sistema de Tabs

**Inventario (11 pestañas):**

1. Equipos
2. Mantenimiento
3. Servicios técnicos
4. Métodos de trabajo
5. Layout de planta
6. Software
7. Materiales
8. Inversiones
9. Talento humano
10. Disciplinas/Saberes
11. Resumen & Validación

**Profiles (4 pestañas):** ⭐ NUEVO

1. Evaluaciones (Assessments)
2. Preguntas (Catálogo)
3. Respuestas (Historial)
4. Llenar evaluación (Formulario agrupado por dimensiones)

**Navegación sin recarga:**

```html
<a href="?tab=equipment" hx-get="..." hx-target="#content" hx-push-url="true">
```

### Patrón CRUD Factory

Generación automática de vistas CRUD mediante factory pattern:

```python
equipment_list, equipment_create, equipment_update, equipment_delete = crud_factory(
    model=Equipment,
    form_class=EquipmentForm,
    list_template="inventory/equipment/_table.html",
    form_template="inventory/equipment/_form_modal.html",
    event_name="equipment:refresh",
    qs_by_company=lambda company: Equipment.objects.filter(company=company),
    company_from_obj=lambda obj: obj.company,
    before_create=lambda obj, company, form: setattr(obj, "company", company),
)
```

**Ventajas:**

- DRY: Elimina código repetitivo
- Consistencia: Mismo comportamiento en todos los CRUDs
- Mantenibilidad: Cambios centralizados
- HTMX-ready: Respuestas 204 con `HX-Trigger` para refrescar

### Sistema de Diseño

**Paleta de colores corporativa:**

```javascript
colors: {
  brand: '#0f7a4a',       // Verde principal
  brandDark: '#0b5e39',   // Verde oscuro
  teal: '#2ca67a',        // Verde medio
  mint: '#b5ebcf',        // Verde claro
  accent: '#f59e0b',      // Acento naranja
  ink: '#0f172a',         // Texto
}
```

**Componentes Tailwind personalizados:**

- `.btn`, `.btn-primary`, `.btn-outline`, `.btn-ghost`
- `.link` - Enlaces corporativos
- `.input` - Inputs con focus ring verde
- `.pill` - Variante redondeada

## 🔧 Configuración y Deployment

### Variables de Entorno

```bash
# Django Core
DJANGO_SECRET_KEY=<secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,www.example.com

# Database (PostgreSQL)
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=<password>
DB_HOST=db-postgresql-nyc3-12345.ondigitalocean.com
DB_PORT=25060

# Localization
LANGUAGE_CODE=es-co
TIME_ZONE=America/Bogota
```

### Base de Datos

**PostgreSQL con SSL obligatorio:**

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "sslmode": "require",  # DigitalOcean Managed DB
        },
    }
}
```

### Deployment en DigitalOcean

**Stack de producción:**

1. **Droplet Ubuntu** con systemd
2. **Caddy** como reverse proxy (HTTPS automático)
3. **Gunicorn** como WSGI server
4. **PostgreSQL Managed Database** con backups automáticos

**Servicio systemd:**

```ini
[Unit]
Description=AlimentaTec Django App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/atec
ExecStart=/var/www/atec/.venv/bin/gunicorn portal.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🚀 Instalación y Desarrollo

### Requisitos Previos

- Python 3.10+
- PostgreSQL 14+
- pip / virtualenv

### Setup Local

```bash
# Clonar repositorio
git clone <repo-url>
cd atec

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install django psycopg2-binary python-dotenv django-filters

# Configurar .env
cp .env.example .env
# Editar .env con credenciales locales

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos iniciales (opcional)
python manage.py loaddata db/seeds/*.json

# Ejecutar servidor de desarrollo
python manage.py runserver
```

### Acceso

- **Portal**: <http://localhost:8000>
- **Admin**: <http://localhost:8000/admin>
- **Inventario**: <http://localhost:8000/inventory/{company_id}/>

## 📁 Estructura de URLs y Archivos

### Mapa de Rutas Completo

```python
# ============ PORTAL PRINCIPAL ============
/                                    # Home / Dashboard (CompanyListView)
/admin/                              # Django Admin
/accounts/login/                     # Login
/accounts/logout/                    # Logout

# ============ CORE (apps/core/) ============
# Archivos: models.py (~60 líneas), views.py (~70 líneas), forms.py (~30 líneas)
/                                    # Lista de empresas (CompanyListView)
/companies/<id>/                     # Detalle empresa (CompanyDetailView)
/companies/new/                      # Crear empresa (CompanyCreateView)
/companies/<id>/edit/                # Editar empresa (CompanyUpdateView)

# ============ INVENTORY (apps/inventory/) ============
# Archivos: models.py (~450 líneas), views.py (~280 líneas), forms.py (~380 líneas)
/inventory/manage/<company_id>/      # Vista principal con tabs

# Equipos (4 endpoints)
/inventory/equipment/<company_id>/list/
/inventory/equipment/<company_id>/new/
/inventory/equipment/<pk>/edit/
/inventory/equipment/<pk>/delete/

# Mantenimiento (4 endpoints)
/inventory/maintenance/<company_id>/list/
/inventory/maintenance/<company_id>/new/
/inventory/maintenance/<pk>/edit/
/inventory/maintenance/<pk>/delete/

# Servicios Técnicos (4 endpoints)
/inventory/services/<company_id>/list/
/inventory/services/<company_id>/new/
/inventory/services/<pk>/edit/
/inventory/services/<pk>/delete/

# Métodos de Trabajo (4 endpoints)
/inventory/methods/<company_id>/list/
/inventory/methods/<company_id>/new/
/inventory/methods/<pk>/edit/
/inventory/methods/<pk>/delete/

# Layout de Planta (4 endpoints)
/inventory/layout/<company_id>/list/
/inventory/layout/<company_id>/new/
/inventory/layout/<pk>/edit/
/inventory/layout/<pk>/delete/

# Software (4 endpoints)
/inventory/software/<company_id>/list/
/inventory/software/<company_id>/new/
/inventory/software/<pk>/edit/
/inventory/software/<pk>/delete/

# Materiales (4 endpoints)
/inventory/materials/<company_id>/list/
/inventory/materials/<company_id>/new/
/inventory/materials/<pk>/edit/
/inventory/materials/<pk>/delete/

# Inversiones (4 endpoints)
/inventory/investments/<company_id>/list/
/inventory/investments/<company_id>/new/
/inventory/investments/<pk>/edit/
/inventory/investments/<pk>/delete/

# Talento Humano (4 endpoints)
/inventory/workforce/<company_id>/list/
/inventory/workforce/<company_id>/new/
/inventory/workforce/<pk>/edit/
/inventory/workforce/<pk>/delete/

# Disciplinas/Saberes (4 endpoints)
/inventory/disciplines/<company_id>/list/
/inventory/disciplines/<company_id>/new/
/inventory/disciplines/<pk>/edit/
/inventory/disciplines/<pk>/delete/

# ============ PROFILES (apps/profiles/) ⭐ NUEVO ============
# Archivos: models.py (~110 líneas), views.py (~240 líneas), forms.py (~100 líneas)
/profiles/<company_id>/              # Vista principal con tabs
/profiles/<company_id>/assessments/  # Lista de evaluaciones
/profiles/<company_id>/assessments/new/  # Crear evaluación
/profiles/<company_id>/questions/    # Catálogo de preguntas
/profiles/<company_id>/responses/    # Respuestas de evaluaciones
/profiles/<company_id>/assessments/<uuid>/fill/  # Llenar evaluación
```

### Detalle de Archivos por Módulo

#### Core (apps/core/)

- `models.py` (~60 líneas) - Organization, Company, AnalystCompany
- `views.py` (~70 líneas) - CBVs con CompanyScopeMixin
- `forms.py` (~30 líneas) - CompanyForm
- `selectors.py` (~20 líneas) - get_allowed_company_ids (RLS)
- `permissions.py` (~60 líneas) - CompanyScopeMixin, require_company_access
- `admin.py` (~40 líneas) - Admin customizado
- `urls.py` (~14 líneas) - 4 rutas

#### Inventory (apps/inventory/)

- `models.py` (~450 líneas) - 15 modelos (Equipment, Material, Investment, etc.)
- `views.py` (~280 líneas) - CRUD factory + 40 vistas generadas
- `forms.py` (~380 líneas) - 10 formularios con Tailwind styling
- `urls.py` (~110 líneas) - 44 endpoints HTMX
- `admin.py` (~80 líneas) - Registro de modelos

#### Profiles (apps/profiles/) ⭐ NUEVO

- `models.py` (~110 líneas) - Question, Assessment, Response (UUID-based)
- `views.py` (~240 líneas) - 6 vistas con agrupación por dimensiones
- `forms.py` (~100 líneas) - AssessmentForm, QuestionForm, ResponseForm
- `urls.py` (~17 líneas) - 6 endpoints
- `admin.py` (~50 líneas) - Admin para catálogo de preguntas
- `templatetags/profiles_extras.py` (~20 líneas) - Filtros custom

#### Accounts (apps/accounts/)

- `models.py` (~10 líneas) - User con UUID primary key
- `admin.py` (~15 líneas) - UserAdmin customizado

#### Common (apps/common/)

- `context_processors.py` (~10 líneas) - PROGRAM context

### Resumen de Endpoints

| Módulo | Endpoints | Archivos Python | Líneas de Código |
|--------|-----------|-----------------|------------------|
| Core | 4 | 6 | ~280 |
| Inventory | 44 | 5 | ~1,300 |
| Profiles | 6 | 6 | ~530 |
| Accounts | 0 | 2 | ~25 |
| **TOTAL** | **54** | **19** | **~2,135** |

## 🧪 Testing y Calidad

### Estructura de Tests

``` batch
apps/
├── core/
│   └── tests.py
├── inventory/
│   └── tests.py
└── accounts/
    └── tests.py
```

### Ejecutar Tests

```bash
python manage.py test
python manage.py test apps.inventory  # Tests específicos
```

## 📦 Dependencias Principales

``` batch
Django==5.2.7
psycopg2-binary>=2.9
python-dotenv>=1.0
django-filters>=23.0
```

## 🔄 Flujo de Trabajo

### Ciclo de Vida de Datos

1. **Registro de Empresa** (Admin/Advisor)
   - Crear Organization
   - Crear Company con datos básicos
   - Asignar Advisor

2. **Asignación de Analistas**
   - Crear AnalystCompany (M2M)
   - Analista obtiene acceso RLS

3. **Captura de Inventario** (Analyst/Advisor)
   - Navegar a `/inventory/<company_id>/`
   - Completar tabs de inventario
   - CRUD vía modales HTMX

4. **Validación y Reportes**
   - Tab "Resumen & Validación"
   - Exportación de datos (futuro)

## 🛠️ Características Técnicas Destacadas

### 1. CRUD Factory Pattern

Generación automática de vistas CRUD con soporte HTMX integrado.

- 40+ vistas generadas automáticamente en inventory
- Patrón DRY con callbacks configurables
- Eventos HTMX personalizados por módulo

### 2. Row-Level Security

Implementación de RLS a nivel de aplicación sin dependencias externas.

- Selector pattern con `get_allowed_company_ids`
- CompanyScopeMixin para CBVs
- Decorator `@require_company_access` para FBVs

### 3. Dynamic Form Filtering

Formularios que filtran opciones según contexto (ej: equipos por empresa).

- `form_kwargs_fn` en CRUD factory
- Filtrado de ForeignKeys por company

### 4. HTMX-Driven Modals

Modales dinámicos sin JavaScript custom, solo atributos HTMX.

- Respuestas 204 con `HX-Trigger`
- Eventos `modal:close` para cerrar automáticamente

### 5. Tailwind CDN + Custom Config

Configuración inline de Tailwind con paleta corporativa.

- TailwindModelForm base class
- Clases reutilizables (.btn, .input, .link)

### 6. Multi-Tenant Ready

Arquitectura preparada para multi-tenancy vía Organization.

- COMPANY_MODEL dinámico con `get_model`
- Lazy loading de modelos relacionados

### 7. UUID Primary Keys

Modelos profiles usan UUID para mayor seguridad.

- Question, Assessment, Response con UUID
- Previene enumeración de recursos

### 8. Agrupación Dinámica de Datos

Agrupación de preguntas por dimensión/subdimensión.

- `defaultdict` anidado para estructuras jerárquicas
- Conversión a dict normal para templates

### 9. Transaction Atomic

Guardado transaccional de respuestas múltiples.

- `@transaction.atomic()` en assessment_fill
- Rollback automático en caso de error

### 10. Type Hints y Type Safety

Uso de `cast()` para type checking con Pylance.

- Modelos dinámicos con type hints
- Decimal para campos monetarios/scores

## 📈 Roadmap y Extensiones

### Implementado

- ✅ Autenticación y RLS
- ✅ CRUD completo de inventario (11 módulos, 44 endpoints)
- ✅ Sistema de tabs con HTMX
- ✅ Formularios dinámicos
- ✅ Diseño corporativo responsive
- ✅ Módulo de Profiles (Perfiles de Innovación/Tecnología) ⭐ NUEVO
- ✅ Evaluaciones con preguntas agrupadas por dimensiones
- ✅ UUID primary keys para seguridad
- ✅ Template tags custom
- ✅ Transaction atomic para guardado múltiple

### En Desarrollo

- 🔄 API REST (estructura creada)
- 🔄 Generación de reportes PDF
- 🔄 Exportación Excel
- 🔄 Dashboard analítico
- 🔄 Cálculo de scores ponderados en Profiles
- 🔄 Visualización de resultados (gráficos radar)

### Futuro

- 📋 Auditoría de cambios
- 📋 Gestión documental
- 📋 Diagnósticos empresariales
- 📋 Notificaciones por email
- 📋 Integración con BI
- 📋 Comparación de evaluaciones en el tiempo
- 📋 Benchmarking entre empresas

## 👥 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **Superuser** | Acceso total, gestión de usuarios |
| **Advisor** | Empresas asignadas como advisor, CRUD inventario |
| **Analyst** | Empresas asignadas vía AnalystCompany, CRUD inventario |
| **Staff** | Acceso al Django Admin |

## 📞 Contacto y Soporte

**Programa:** AlimentaTec Antioquia  
**Organización:** CIB - Centro de Innovación y Bienestar  
**Email:** <alimentatec@cib.org.co>  
**Teléfono:** +57 323 586 5867

## 📄 Licencia

Proyecto desarrollado para la Gobernación de Antioquia y el CIB.  
Todos los derechos reservados © 2024.

---

**Desarrollado con ❤️ para el sector alimentario de Antioquia**
