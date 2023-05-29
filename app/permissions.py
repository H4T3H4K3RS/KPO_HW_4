from rest_framework.permissions import BasePermission

from kpoOrderProject import settings


class IsManager(BasePermission):
    """
    Permission class for checking if the user is a manager.

    A user is considered a manager if they have all the required permissions.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the required permissions to be considered a manager.

        Args:
            request (HttpRequest): The incoming request.
            view: The view being accessed.

        Returns:
            bool: True if the user is a manager, False otherwise.
        """
        user = request.user
        required_permissions = [
            'app.add_dish', 'app.change_dish', 'app.delete_dish', 'app.view_dish',
            'app.add_order', 'app.change_order', 'app.delete_order', 'app.view_order',
            'app.add_orderdish', 'app.change_orderdish', 'app.delete_orderdish', 'app.view_orderdish'
        ]
        return user and user.is_authenticated and (
                user.is_superuser or all(user.has_perm(permission) for permission in required_permissions))


class IsBotOrAuthenticated(BasePermission):
    """
    Permission class for allowing bot authentication or authenticated users.

    This permission allows requests to be authenticated either with a bot authorization header or by an authenticated user.
    """

    def has_permission(self, request, view):
        """
        Check if the request has bot authentication header or if the user is authenticated.

        Args:
            request (HttpRequest): The incoming request.
            view: The view being accessed.

        Returns:
            bool: True if the request is authorized, False otherwise.
        """
        bot_auth_header = request.headers.get('Authorization', None) == settings.BOT_SECRET
        return bot_auth_header or (request.user and request.user.is_authenticated)
