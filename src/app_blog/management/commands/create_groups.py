from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default user groups."

    def handle(self, *args, **options):
        groups = [
            "Viewer",
            "Editor",
            "Admin",
        ]

        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        self.stdout.write(self.style.SUCCESS("Groups created successfully."))
