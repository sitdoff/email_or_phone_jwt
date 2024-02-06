from djoser.serializers import UserCreateSerializer

from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Customuser's serializer.
    """

    class Meta:
        """
        Customuser serializer's meta class.
        """

        model = CustomUser
        fields = ("id", "username", "email", "phone", "is_active", "is_superuser", "password")
