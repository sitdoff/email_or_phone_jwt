from django.db.models import Q
from django.http import HttpRequest

from .models import CustomUser


class AuthBackend:
    """
    An authentication class that allows you to use email or phone instead of a username.
    """

    supports_object_permissions = True
    supports_anonimous_user = False
    supports_inactive_user = False

    def get_user(self, user_id: int) -> CustomUser | None:
        """
        Gets the user by user_id
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(self, request: HttpRequest, username: str, password: str) -> CustomUser | None:
        """
        Searches for a user using username, email or phone number.
        """
        try:
            user = CustomUser.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
        except CustomUser.DoesNotExist:
            return None

        return user if user.check_password(password) else None
