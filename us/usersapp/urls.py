from django.urls import include, path
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
]
