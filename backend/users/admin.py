# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your custom user model with the admin site
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define how your CustomUser model is displayed in the admin
    # You might want to customize list_display, fieldsets, etc.
    # based on any extra fields you add to CustomUser.
    pass

# If you had other models in the users app, you would register them here too:
# from .models import OtherUserModel
# admin.site.register(OtherUserModel)