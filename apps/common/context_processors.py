from django.conf import settings

def program(request):
    """Inyecta PROGRAM en todos los templates."""
    return {"PROGRAM": getattr(settings, "PROGRAM", {})}
