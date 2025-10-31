# apps/core/selectors.py
from typing import Set, Union, Optional
from django.contrib.auth.models import AbstractUser, AnonymousUser
from .models import Company, AnalystCompany


def get_allowed_company_ids(user: Optional[Union[AbstractUser, AnonymousUser]]) -> Set[int]:
    """
    Devuelve el conjunto de IDs de Company a los que el usuario puede acceder.
    - superuser: acceso total (set vacío especial -> usa None para significar 'sin filtro')
    - analista asignado (AnalystCompany)
    - advisor asignado en Company.advisor
    """
    if not user or not getattr(user, "is_authenticated", False):
        return set()
    if getattr(user, "is_superuser", False):
        return set()

    assigned = AnalystCompany.objects.filter(user=user).values_list("company_id", flat=True)
    advised = Company.objects.filter(advisor=user).values_list("id", flat=True)
    return set(assigned) | set(advised)
