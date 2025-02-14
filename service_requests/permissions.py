from rest_framework import permissions

class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Customers can create/update their own requests.
    Support reps can only update requests.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET for all
        if request.user.is_staff:  # Support reps can update
            return request.method in ['PUT']
        return obj.customer == request.user  # Customers can edit/delete their own requests

class IsCustomerOnly(permissions.BasePermission):
    """
    Only customers can delete their requests.
    """
    def has_object_permission(self, request, view, obj):
        return request.method == "DELETE" and obj.customer == request.user
