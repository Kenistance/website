# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    UserProfileView,
    LogoutView,
    PasswordResetRequestView, # New
    SetNewPasswordView        # New
)

urlpatterns = [
    # JWT authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User management endpoints
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # Password Reset Endpoints (New)
    path('request-password-reset/', PasswordResetRequestView.as_view(), name='request_password_reset'),
    path('reset-password-confirm/', SetNewPasswordView.as_view(), name='reset_password_confirm'),
]