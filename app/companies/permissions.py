from rest_framework import permissions

class IsCompanyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsCompanyOwnerOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        company = getattr(obj, 'company', None) or obj
        return (
            company.owner == request.user
            or request.user in company.employees.all()
        )