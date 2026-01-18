# 2. third party imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing basic user profile data.

    Uses `fullname` as a friendly alias for the Django `username` field.
    """

    fullname = serializers.CharField(source="username")

    class Meta:
        """
        Serializer metadata.
        """
        model = User
        fields = ["id", "email", "fullname"]

    def validate_fullname(self, value):
        """
        Ensure the username is unique (case-insensitive).

        Excludes the current instance during updates.
        """
        if User.objects.filter(username__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Username already taken.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Validates:
    - password length
    - password confirmation
    - unique username (fullname) and email
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False
    )
    repeated_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )
    fullname = serializers.CharField(
        source='username',
        required=True
    )
    email = serializers.EmailField(required=True)

    class Meta:
        """
        Serializer metadata.
        """
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]

    def validate(self, attrs):
        """
        Ensure both passwords match.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords must match."}
            )
        return attrs

    def validate_fullname(self, value):
        """
        Ensure the username is unique (case-insensitive).
        """
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        """
        Ensure the email is unique (case-insensitive).
        """
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        validated_data.pop("repeated_password")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user via email and password.

    Resolves the user by email and then authenticates using the user's username
    (compatible with Django's default authentication backend).
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate credentials and attach the authenticated user to `attrs`.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Both email and password are required."
            )

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        user = authenticate(
            request=self.context.get("request"),
            username=user.username,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs
