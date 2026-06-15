"""
User Views
Handles user registration, login, logout, and basic user management.
"""

from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.backends import EmailBackend
from user.models import User
from user.serializers import LoginSerializer, UserResponseSerializer, UserSerializer


# Register — anyone can create an account

class RegisterView(CreateAPIView):
    """
    Returns the created user info (without password).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # 1: Validate the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2: Save the user (password gets hashed automatically)
        user = serializer.save()

        #3: Return user info
        response_data = UserResponseSerializer(user).data
        response_data["message"] = "Registration successful!"

        return Response(response_data, status=status.HTTP_201_CREATED)


# Login — email + password

@extend_schema(request=LoginSerializer, responses={200: UserResponseSerializer})
class LoginView(APIView):
    """
    Anyone can login with registered credentials
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1: Check that email and password are provided
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # 2: Try to find the user and check password
        backend = EmailBackend()
        user = backend.authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3: Log the user in (this creates a session cookie)
        login(request, user, backend='user.backends.EmailBackend')

        # 4: Return user info
        response_data = UserResponseSerializer(user).data
        response_data["message"] = "Login successful!"

        return Response(response_data, status=status.HTTP_200_OK)



# Logout — clears the session

@extend_schema(request=None, responses={200: None})
class LogoutView(APIView):
    """
    Clears the session cookie. User will need to login again.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)

        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


# User CRUD — list, view, update, delete users

class UserViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for users (must be logged in).
    Supports search via ?search=<query> on name, email, username.
    """

    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    lookup_field = "user_id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email_id", "user_name"]
    ordering_fields = ["creation_date", "user_name", "first_name"]
    ordering = ["-creation_date"]

    def get_serializer_class(self):
        """Use read serializer for list/retrieve, write serializer for create/update."""
        if self.action in ("list", "retrieve"):
            return UserResponseSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        """
        mark the user as inactive instead of removing.
        """
        instance.is_active = False
        instance.save(update_fields=["is_active", "updation_date"])

    def destroy(self, request, *args, **kwargs):
        """return user deactivation message."""
        instance = self.get_object()

        if not instance.is_active:
            return Response(
                {"detail": "User is already inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_destroy(instance)
        return Response(
            {"detail": f"User '{instance.user_name}' has been deactivated."},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        """Create a user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update a user"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
