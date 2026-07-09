from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustumUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    ordering = ("email", )
    search_fields = ("email", )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("permissions", {"fields": ("is_staff", "is_active",
         "is_superuser", "groups", "user_permissions")}),
        ("important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")
        }),
    )
