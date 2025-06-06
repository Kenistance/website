# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model # Best practice for accessing the user model
from django.contrib.auth.password_validation import validate_password

# Get the custom user model defined in settings.AUTH_USER_MODEL
CustomUser = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer): # Renamed for clarity (previously CustomUserSerializer)
    """
    Serializer for the CustomUser model.
    Used for retrieving and updating user details (excluding sensitive fields like password).
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'username', 'email', 'is_staff', 'date_joined'] # Made username and email read-only for profile updates

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
        # If you have specific email validation beyond Django's default, add it here
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
        return attrs

    def create(self, validated_data):
        # This is where the user is created.
        # The logic here was generally correct for creating a user.
        # The previous 'no users in admin' issue was likely due to missing URL configuration
        # or admin registration, not this create method itself.
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user