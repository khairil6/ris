# data/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Institution, User


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "hl7_facility_code", "dicom_station_name")
    search_fields = ("name", "hl7_facility_code")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Show the usual User fields, plus 'institution', 'role', 'dicom_ae_title'
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Institution & Role", {"fields": ("institution", "role", "dicom_ae_title")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "institution", "role", "dicom_ae_title", "password1", "password2"),
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "institution", "role", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "institution", "role")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
