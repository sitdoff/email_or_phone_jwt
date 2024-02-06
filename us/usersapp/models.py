from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    User's custom model
    """

    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    password = models.CharField("password", max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        """
        CustomUser meta class
        """

        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return (self.username or self.email or self.phone) + (
            " (Administrator)" if self.is_superuser else ""
        )
