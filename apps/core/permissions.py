# apps/core/permissions.py
from typing import Set, Any, cast
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property
from django.views.generic.base import View  
from .selectors import get_allowed_company_ids

class CompanyScopeMixin(View):  
    """
    Mixin para CBVs: aplica un filtro por empresas permitidas.

    Requiere que el modelo tenga:
      - FK 'company' (por defecto) O
      - sea Company (en cuyo caso filtramos por id).
    """
    company_field = "company"
    is_company_model = False

    @cached_property
    def _allowed_ids(self) -> Set[int]:
        user = getattr(self.request, "user", None)
        return get_allowed_company_ids(user)

    def filter_queryset_by_scope(self, qs):
        if getattr(self.request.user, "is_superuser", False):
            return qs
        if self.is_company_model:
            return qs.filter(id__in=self._allowed_ids)
        return qs.filter(**{f"{self.company_field}_id__in": self._allowed_ids})

    # Para ListView
    def get_queryset(self):
        parent = cast(Any, super()) 
        qs = parent.get_queryset() 
        return self.filter_queryset_by_scope(qs)

    # Para DetailView
    def get_object(self, queryset=None):
        parent = cast(Any, super())
        obj = parent.get_object(queryset)
        if getattr(self.request.user, "is_superuser", False):
            return obj
        company_id = getattr(
            obj,
            "id" if self.is_company_model else f"{self.company_field}_id",
            None,
        )
        if company_id in self._allowed_ids:
            return obj
        raise PermissionDenied("No tienes acceso a esta empresa.")


def require_company_access(get_company_id):
    """
    Decorator para FBVs. 'get_company_id(request, *args, **kwargs)' debe retornar el company_id del recurso.
    """
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            allowed = get_allowed_company_ids(user)
            cid = get_company_id(request, *args, **kwargs)
            if cid in allowed:
                return view_func(request, *args, **kwargs)
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("No tienes acceso a esta empresa.")
        return _wrapped
    return decorator
