from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

ROLE_DEFS = {
    "READER":  {"perms": ["view"]},
    "EDITOR":  {"perms": ["view", "add", "change"]},
    "LOCAL_ADMIN": {"perms": ["view", "add", "change", "delete"]},
}

# Aplica a estos modelos (app_label, model_name)
TARGET_MODELS = [
    ("core", "organization"),
    ("core", "company"),
    ("core", "analystcompany"),
]

def perm_codename(action, model_name):
    return f"{action}_{model_name}"

class Command(BaseCommand):
    help = "Create base groups (RBAC) and assign model permissions."

    def handle(self, *args, **kwargs):
        created = []
        for role, cfg in ROLE_DEFS.items():
            group, _ = Group.objects.get_or_create(name=role)
            for app_label, model in TARGET_MODELS:
                model_cls = apps.get_model(app_label, model)
                for action in cfg["perms"]:
                    code = perm_codename(action, model)
                    try:
                        perm = Permission.objects.get(
                            content_type__app_label=app_label,
                            codename=code
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f"Permission not found: {app_label}.{code}"
                        ))
                        continue
                    group.permissions.add(perm)
            group.save()
            created.append(group.name)

        self.stdout.write(self.style.SUCCESS(
            f"Groups initialized: {', '.join(created)}"
        ))
        self.stdout.write(self.style.SUCCESS(
            "Remember: set is_superuser=True for your SUPERADMIN account."
        ))
