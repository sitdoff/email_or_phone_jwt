from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    CustomUser manager
    """

    use_in_migrations = True

    def _create_user(
        self,
        username: str = None,
        email: str = None,
        phone: str = None,
        password: str = None,
        **extra_fields: dict[str, Any]
    ) -> "CustomUser":
        """
        Creates and saves a User with given data
        """
        if username is None and (email is None and phone is None):
            raise ValueError("email or phone must be set")

        if email:
            email = self.normalize_email(email)
            username = username or email
            user = self.model(username=username, email=email, **extra_fields)
        elif phone:
            username = username or phone
            user = self.model(username=username, phone=phone, **extra_fields)
        else:
            raise ValueError("email or phone must be set")

        if extra_fields.get("is_superuser") is None:
            user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str = None,
        email: str = None,
        phone: str = None,
        password: str = None,
        **extra_fields: dict[str, Any]
    ) -> "CustomUser":
        """
        Creates a regular user.
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields["is_active"] = True
        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(
        self,
        username: str = None,
        email: str = None,
        phone: str = None,
        password: str = None,
        **extra_fields: dict[str, Any]
    ) -> "CustomUser":
        """
        Creates a superuser.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self._create_user(username, email, phone, password, **extra_fields)
