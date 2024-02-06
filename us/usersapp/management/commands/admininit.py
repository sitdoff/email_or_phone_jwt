import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from usersapp.models import CustomUser

load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            username = os.getenv("SUPERUSER_USERNAME")
            email = os.getenv("SUPERUSER_EMAIL")
            password = os.getenv("SUPERUSER_PASSWORD")
            print(f"Creating account for {username} ({email})")
            admin = CustomUser.objects.create_superuser(
                email=email, username=username, password=password
            )
            admin.save()
        else:
            print("Admin account already initialized")
