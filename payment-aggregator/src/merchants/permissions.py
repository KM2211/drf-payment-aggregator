from rest_framework.permissions import BasePermission

class IsAuthenticatedMerchant(BasePermission):
    """
    Allows access only to authenticated merchants
    """

    def has_permission(self, request, view):
        return bool(request.user)
