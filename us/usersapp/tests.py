from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser

# Create your tests here.
request_user_data = {
    "email": "user@mail.com",
    "password": "user_password",
    "phone": "+71234567890",
}


class RegistrationTestCase(TestCase):
    """
    Testing user creation using the /auth/users/ endpoint
    """

    def test_post_email_create_user(self):
        """
        Tests user creation using email.
        """
        data = {
            "email": request_user_data["email"],
            "password": request_user_data["password"],
        }
        response = self.client.post(path=reverse("customuser-list"), data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["username"], data["email"], "Username wrong!")
        self.assertEqual(response_data["email"], data["email"], "Email wrong!")
        self.assertIsNone(response_data["phone"], "Phone wrong!")

        user = CustomUser.objects.get(username=data["email"])
        self.assertEqual(user.username, data["email"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_post_phone_create_user(self):
        """
        Tests user creation using phone.
        """
        data = {
            "phone": request_user_data["phone"],
            "password": request_user_data["password"],
        }
        response = self.client.post(path=reverse("customuser-list"), data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["username"], data["phone"], "Username wrong!")
        self.assertEqual(response_data["phone"], data["phone"], "Phone wrong!")
        self.assertIsNone(response_data["email"], "Email wrong!")

        user = CustomUser.objects.get(username=data["phone"])
        self.assertEqual(user.username, data["phone"])
        self.assertEqual(user.phone, data["phone"])
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)


class JWTTestCase(TestCase):
    """
    Testing JWT-tokens creation using the /jwt/create/ endpoint
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create users before tests. Set self.cliet = APIClient().
        """
        cls.client = APIClient()

        cls.user_with_email = CustomUser.objects.create_user(
            email=request_user_data["email"],
            password=request_user_data["password"],
        )
        cls.user_with_phone = CustomUser.objects.create_user(
            phone=request_user_data["phone"],
            password=request_user_data["password"],
        )

    def get_respose_get_method(self, url_name: str, headers=None):
        """
        Returns a response to a GET request.
        """
        response = self.client.get(reverse(url_name), headers=headers)
        return response

    def get_respose_post_method(self, url_name: str, **extra_fields: dict[str, str]):
        """
        Returns a response to a POST request.
        """
        response = self.client.post(
            reverse(url_name),
            data=extra_fields,
            format="json",
        )
        return response

    def get_jwt_tokens(self, **extra_fields):
        """
        Return access and refresh token
        """
        response = self.get_respose_post_method("jwt-create", **extra_fields)
        response_data = response.json()
        return response_data["access"], response_data["refresh"]

    def test_create_jwt_by_user_without_username(self):
        """
        Tests the creation of a token without passing the username in the request.
        """
        response = self.get_respose_post_method("jwt-create", password=request_user_data["password"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_jwt_by_user_without_password(self):
        """
        Tests the creation of a token without passing the password in the request.
        """
        response = self.get_respose_post_method("jwt-create", username=request_user_data["email"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.get_respose_post_method("jwt-create", username=request_user_data["phone"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_jwt_by_user_with_email(self):
        """
        Tests the creation of a token using mail as a username.
        """
        response = self.get_respose_post_method(
            "jwt-create", username=request_user_data["email"], password=request_user_data["password"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_create_jwt_by_user_with_phone(self):
        """
        Tests the creation of a token using phone as a username.
        """
        response = self.get_respose_post_method(
            "jwt-create", username=request_user_data["phone"], password=request_user_data["password"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_user_list_unauthorized(self):
        """
        Testing a request from an unauthorized user.
        """
        response = self.get_respose_get_method("customuser-list")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})

    def test_get_users_list_with_autorization(self):
        """
        Testing a request from a user with access token in header.
        """
        acces_token, _ = self.get_jwt_tokens(
            username=request_user_data["email"], password=request_user_data["password"]
        )
        headers = {"Authorization": "Bearer " + acces_token}
        response = self.get_respose_get_method("customuser-list", headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """
        Testing refresh token.
        """
        acces_token, refresh_token = self.get_jwt_tokens(
            username=request_user_data["email"], password=request_user_data["password"]
        )
        response = self.get_respose_post_method("jwt-refresh", refresh=refresh_token)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_data)
        self.assertNotIn("refresh", response_data)
        new_access_token = response_data["access"]
        self.assertNotEqual(acces_token, new_access_token)
