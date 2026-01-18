# 2. third party imports
from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

# 3. lokal imports
from .serializers import (
    UserProfileSerializer,
    RegistrationSerializer,
    EmailAuthTokenSerializer,
)
from user_auth_app.permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profile access.

    - Admins can access all users.
    - Regular authenticated users can only access their own user object.
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Return a queryset limited to the current user unless the user is an admin.
        """
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(id=user.id)


class RegistrationView(generics.CreateAPIView):
    """
    Create a new user account and return an authentication token.

    Returns:
        201 CREATED: Token and basic user data.
        400 BAD REQUEST: Validation errors.
    """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Register a new user and issue a token for immediate authentication.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(ObtainAuthToken):
    """
    Authenticate a user by email/password and return an auth token.

    Returns:
        200 OK: Token and basic user data.
        400 BAD REQUEST: Invalid credentials or validation errors.
    """

    permission_classes = [AllowAny]
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Validate credentials, then return (or create) a token for the user.
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id,
            }
        )
