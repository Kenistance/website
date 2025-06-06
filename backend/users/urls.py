# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # Used for getting access and refresh tokens (login)
    TokenRefreshView,    # Used for refreshing an expired access token
)
from .views import UserRegistrationView, UserProfileView, LogoutView

urlpatterns = [
    # JWT authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh token
    path('logout/', LogoutView.as_view(), name='logout'), # Logout (requires custom view)

    # User management endpoints
    path('register/', UserRegistrationView.as_view(), name='user_register'), # Registration
    path('profile/', UserProfileView.as_view(), name='user_profile'),       # View/Edit own profile
]