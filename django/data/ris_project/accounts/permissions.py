from rest_framework.permissions import BasePermission

class IsClinicAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CLINIC_ADMIN' or request.user.is_superuser

class IsRadiologist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'RADIOLOGIST' or request.user.is_superuser
