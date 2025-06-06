# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError # Import ValidationError
import logging

logger = logging.getLogger(__name__)

# Get the custom user model defined in settings.AUTH_USER_MODEL
CustomUser = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Used for retrieving and updating user details (excluding sensitive fields like password).
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'is_staff', 'date_joined']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    Takes the user's email address.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password after a reset request.
    Takes the UID, token, and the new password.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    class Meta:
        fields = ['password', 'password2', 'uidb64', 'token']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def save(self):
        try:
            password = self.validated_data['password']
            token = self.validated_data['token']
            uidb64 = self.validated_data['uidb64']

            # Decode the UID
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            # Check if the token is valid for the user
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset link is invalid or has expired.")

            # Set the new password
            user.set_password(password)
            user.save()
            logger.info(f"Password for user {user.username} has been reset successfully.")

            return user
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, DjangoUnicodeDecodeError, ValidationError) as e:
            logger.error(f"Password reset failed: {e}")
            raise serializers.ValidationError("The reset link is invalid or has expired.")