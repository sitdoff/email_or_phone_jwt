from django.contrib import admin

from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
