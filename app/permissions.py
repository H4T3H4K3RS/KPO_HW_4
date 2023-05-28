from rest_framework.permissions import BasePermission


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            required_permissions = [
                'add_dish', 'change_dish', 'delete_dish', 'view_dish',
                'add_order', 'change_order', 'delete_order', 'view_order',
                'add_orderdish', 'change_orderdish', 'delete_orderdish', 'view_orderdish'
            ]
            return all(user.has_perm(permission) for permission in required_permissions)
        return False
