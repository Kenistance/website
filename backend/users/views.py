# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # Import RefreshToken
from .serializers import UserRegistrationSerializer, UserProfileSerializer # Use UserProfileSerializer
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
        user = serializer.save() # Call serializer.save() directly to get the user instance

        # IMPROVEMENT/CLARIFICATION:
        # Previously, the 'no users in admin' issue was *not* directly caused by this view's logic,
        # but by URL routing, admin registration, or migration issues.
        # However, for a more informative frontend response, it's better to return
        # specific user details on successful registration.
        logger.info(f"User {user.username} registered successfully.") # Use 'user' instance
        return Response({
            "message": "User registered successfully.",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
            # You might also generate and return tokens here if desired
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer # FIX: Changed from CustomUserSerializer to UserProfileSerializer
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
            # FIX: Changed from request.data["refresh"] to request.data["refresh_token"]
            # This should match what your frontend sends (commonly 'refresh_token')
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                logger.warning(f"Logout attempt by {request.user.username}: No refresh_token provided.")
                return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.username} logged out successfully (token blacklisted).")
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout failed for user {request.user.username}: {e}")
            return Response({"detail": "Invalid token or logout failed."}, status=status.HTTP_400_BAD_REQUEST)