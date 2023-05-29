from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new User instance.

        Args:
            validated_data: The validated data for user creation.

        Returns:
            User: The created user instance.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def get_role(self, obj):
        """
        Get the user role based on the associated groups.

        Args:
            obj: The user object.

        Returns:
            str: The user role.
        """
        groups = obj.groups.all()
        return "_".join([group.name.lower() for group in groups]) if groups else "client"


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
