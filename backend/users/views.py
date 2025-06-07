# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserProfileSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
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
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(f"User registration attempt for username: {request.data.get('username')}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        logger.info(f"User {user.username} registered successfully.")
        return Response({
            "message": "User registered successfully.",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
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


class PasswordResetRequestView(generics.GenericAPIView):
    """
    API endpoint for requesting a password reset.
    Sends an email with a reset link to the user.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            # Construct the reset link (adjust 'frontend_url' as per your frontend application)
            frontend_url = getattr(settings, 'FRONTEND_PASSWORD_RESET_URL', 'http://localhost:3000/reset-password')
            reset_link = f"{frontend_url}/{uidb64}/{token}/"

            # Create simple email content without template
            email_subject = "Password Reset Request"
            email_body = f"""
            Hi {user.username},

            You requested a password reset for your account.

            Click the link below to reset your password:
            {reset_link}

            If you didn't request this, please ignore this email.

            Best regards,
            Your Website Team
            """

            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email}.")
            return Response({"detail": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.warning(f"Password reset request for non-existent email: {email}")
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error sending password reset email to {email}: {e}")
            return Response({"detail": "Error sending password reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SetNewPasswordView(generics.GenericAPIView):
    """
    API endpoint for setting a new password using the UID and token.
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # The save method in the serializer handles password update
        logger.info(f"Password for user {user.username} has been successfully reset.")
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)