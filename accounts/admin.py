from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    search_fields = ("first_name", "last_name", "email")
    ordering = None
    list_display = ("id", "email", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_verified",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        # (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_verified",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    # form = UserChangeForm
    # add_form = UserCreationForm
    model = CustomUser


# class ProfileAdmin(UserAdmin):
#     search_fields = ("first_name", "last_name", "email")
#     ordering = None
#     list_display = ("id","email")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
