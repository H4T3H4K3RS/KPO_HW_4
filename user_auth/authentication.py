import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class.

    This class handles the authentication of requests using JWT (JSON Web Token).
    """

    def authenticate(self, request):
        """
        Authenticates the request using JWT.

        Args:
            request (HttpRequest): The incoming request object.

        Returns:
            tuple: A tuple containing the authenticated user and any additional information (None in this case).
                   If authentication fails, None is returned.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            auth_header = auth_header.split(' ')
            token = auth_header[1] if len(auth_header) > 1 else auth_header[0]

            # Check if the token is the bot secret token
            if token == settings.BOT_SECRET:
                return None, None

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return user, None

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except (jwt.DecodeError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token')


class EmailBackend(ModelBackend):
    """
    Custom Email Backend class.

    This class handles authentication using email as the username field.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates the user using email and password.

        Args:
            request (HttpRequest): The incoming request object.
            username (str): The username/email of the user.
            password (str): The password of the user.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user if successful, None otherwise.
        """
        email = kwargs.get('email', username)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
