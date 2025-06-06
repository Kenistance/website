# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows new users to sign up.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Allow anyone to register

    def post(self, request, *args, **kwargs):
        logger.info(f"User registration attempt for username: {request.data.get('username')}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"User {serializer.instance.username} registered successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can access their profile

    def get_object(self):
        # Return the currently authenticated user's profile
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving profile for user: {request.user.username}")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating profile for user: {request.user.username}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance, otherwise
            # the updated object might not be reflected in a subsequent retrieve.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class LogoutView(APIView):
    """
    API endpoint for logging out a user by blacklisting their refresh token.
    Requires an authenticated user and a valid refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Assuming the refresh token is sent in the request body
            # Or you might get it from a cookie or header if implemented that way
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.username} logged out successfully (token blacklisted).")
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout failed for user {request.user.username}: {e}")
            return Response({"detail": "Invalid token or logout failed."}, status=status.HTTP_400_BAD_REQUEST)